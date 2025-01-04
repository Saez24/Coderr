from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from profile_app.models import Profile
from rest_framework import serializers


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'user', 'title', 'revisions',
                  'delivery_time_in_days', 'price', 'features', 'offer_type', 'user']


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at',
                  'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']

    def to_representation(self, instance):
        queryset_called = self.context.get('queryset_called', False)
        data = super().to_representation(instance)
        if queryset_called == True:
            limited_data = generate_data_details_url(data)
        else:
            limited_data = generate_data_details_all(data)
        return limited_data

    def create(self, validated_data):
        print("Validated Data:", validated_data)  # Debugging
        details_data = validated_data.pop('details', [])

    # Konvertiere die Datentypen für Details
        for detail in details_data:
            detail['revisions'] = int(detail['revisions'])
            detail['delivery_time_in_days'] = int(
                detail['delivery_time_in_days'])
            detail['price'] = float(detail['price'])

    # User-ID in Profile-Objekt konvertieren
        user_id = validated_data.pop('user')
        user_profile = Profile.objects.get(id=user_id)

    # Offer erstellen
        offer = Offer.objects.create(user=user_profile, **validated_data)

    # Minimum Werte berechnen
        offer.min_price = min(item['price'] for item in details_data)
        offer.min_delivery_time = min(
            item['delivery_time_in_days'] for item in details_data)
        offer.user_details = generate_user_data(user_profile)

    # Details erstellen
        generate_offer_detail(details_data, offer)
        offer.save()
        return offer

    def perform_create(self, serializer):
        user_profile = Profile.objects.get(
            user=self.request.user)  # Profile-Objekt holen
        serializer.save(user=user_profile)

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', [])

        if details_data:
            # Vorhandene Details löschen
            OfferDetail.objects.filter(user=instance.user).delete()

        # Neue Details hinzufügen
        instance.details = []
        for detail_data in details_data:
            detail_serializer = OfferDetailSerializer(data=detail_data)
            detail_serializer.is_valid(raise_exception=True)
            detail = detail_serializer.save(user=instance.user)

            detail_url = f"/offerdetails/{detail.pk}/"
            instance.details.append({
                "id": detail.pk,
                "url": detail_url,
                "title": detail_data['title'],
                "revisions": detail_data['revisions'],
                "delivery_time_in_days": detail_data['delivery_time_in_days'],
                "price": detail_data['price'],
                "features": detail_data['features'],
                "offer_type": detail_data['offer_type']
            })

    # Andere Felder aktualisieren
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


def generate_offer_detail(details_data, offer):
    for detail_data in details_data:
        print("Creating detail:", detail_data)  # Debugging
        # Nutzer als Primärschlüssel setzen
        detail_data['user'] = offer.user.pk
        detail_serializer = OfferDetailSerializer(data=detail_data)
        if not detail_serializer.is_valid():
            print("Validation Error:", detail_serializer.errors)  # Fehler loggen
            raise ValueError(detail_serializer.errors)  # Fehler werfen
        detail = detail_serializer.save()  # Detail speichern
        detail_url = f"/offerdetails/{detail.pk}/"
        offer.details.append({
            "id": detail.pk,
            "url": detail_url,
            "title": detail_data['title'],
            "revisions": detail_data['revisions'],
            "delivery_time_in_days": detail_data['delivery_time_in_days'],
            "price": detail_data['price'],
            "features": detail_data['features'],
            "offer_type": detail_data['offer_type'],
        })
    offer.save()


def generate_user_data(profile):

    return {
        'first_name': profile.first_name,
        'last_name': profile.last_name,
        'username': profile.username,
    }


def generate_data_details_url(data):
    return {
        "id": data["id"],
        "user": data["user"],
        "title": data["title"],
        "image": data["image"],
        "description": data["description"],
        "created_at": data["created_at"],
        "updated_at": data["updated_at"],
        "details": [
            {
                "id": detail["id"],
                "url": detail["url"],
            }
            for detail in data["details"]
        ],
        "min_price": data["min_price"],
        "min_delivery_time": data["min_delivery_time"],
        "user_details": data["user_details"]
    }


def generate_data_details_all(data):
    return {
        "id": data["id"],
        "user": data["user"],
        "title": data["title"],
        "image": data["image"],
        "description": data["description"],
        "created_at": data["created_at"],
        "updated_at": data["updated_at"],
        "details": [
            {
                "id": detail["id"],
                "title": detail["title"],
                "revisions": detail["revisions"],
                "delivery_time_in_days": detail["delivery_time_in_days"],
                "price": detail["price"],
                "features": detail["features"],
                "offer_type": detail["offer_type"],
            }
            for detail in data["details"]
        ],
        "min_price": data["min_price"],
        "min_delivery_time": data["min_delivery_time"],
        "user_details": data["user_details"]
    }
