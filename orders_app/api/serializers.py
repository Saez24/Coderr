from rest_framework import serializers
from orders_app.models import Order
from offers_app.models import OfferDetail


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer_user', 'business_user', 'title', 'revisions',
                  'delivery_time_in_days', 'price', 'features', 'offer_type', 'status',
                  'created_at', 'updated_at']


class CreateOrderSerializer(serializers.Serializer):
    offer_detail_id = serializers.IntegerField()

    def validate_offer_detail_id(self, value):
        try:
            OfferDetail.objects.get(pk=value)
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError(
                "OfferDetail with this ID does not exist.")
        return value

    def create(self, validated_data):
        offer_detail = OfferDetail.objects.get(
            pk=validated_data['offer_detail_id'])

        # Hole das Profile-Objekt für den customer_user und business_user
        customer_user_profile = self.context['request'].user.profile
        business_user_profile = offer_detail.user  # Dies ist ein Profile-Objekt

        # Erstelle die Bestellung
        order = Order.objects.create(
            customer_user=customer_user_profile,  # Übergib das Profile-Objekt
            business_user=business_user_profile,  # Auch hier das Profile-Objekt
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status="in_progress"
        )

        return order
