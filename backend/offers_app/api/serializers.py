from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from profile_app.models import Profile


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
        if queryset_called:
            limited_data = generate_data_details_url(data)
        else:
            limited_data = generate_data_details_all(data)
        return limited_data

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])

        for detail in details_data:
            detail['revisions'] = int(detail['revisions'])
            detail['delivery_time_in_days'] = int(
                detail['delivery_time_in_days'])
            detail['price'] = float(detail['price'])

        user_id = validated_data.pop('user')
        user_profile = Profile.objects.get(id=user_id)

        offer = Offer.objects.create(user=user_profile, **validated_data)

        offer.min_price = min(item['price'] for item in details_data)
        offer.min_delivery_time = min(
            item['delivery_time_in_days'] for item in details_data)
        offer.user_details = generate_user_data(user_profile)

        generate_offer_detail(details_data, offer)
        offer.save()
        return offer

    def perform_create(self, serializer):
        user_profile = Profile.objects.get(user=self.request.user)
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

        # Minimum Werte berechnen und setzen
            instance.min_price = min(detail['price']
                                     for detail in details_data)
            instance.min_delivery_time = min(
                detail['delivery_time_in_days'] for detail in details_data)

    # Andere Felder aktualisieren
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Sicherstellen, dass min_price und min_delivery_time auch aktualisiert werden, wenn keine neuen Details übergeben werden
        current_details = OfferDetail.objects.filter(user=instance.user)
        if current_details.exists():
            instance.min_price = min(
                detail.price for detail in current_details)
            instance.min_delivery_time = min(
                detail.delivery_time_in_days for detail in current_details)

        instance.save()
        return instance


def generate_offer_detail(details_data, offer):
    for detail_data in details_data:
        detail_data['user'] = offer.user.pk
        detail_serializer = OfferDetailSerializer(data=detail_data)
        if not detail_serializer.is_valid():
            raise ValueError(detail_serializer.errors)
        detail = detail_serializer.save()
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
