from rest_framework import serializers
from django.contrib.auth.models import User
from reviews_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    business_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all())
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating',
                  'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'reviewer']

    def to_internal_value(self, data):
        # Konvertiere `business_user` von einem Objekt in eine ID
        if isinstance(data.get('business_user'), dict):
            data['business_user'] = data['business_user'].get('pk')
        return super().to_internal_value(data)

    def validate(self, data):
        business_user = data.get('business_user')
        reviewer = self.context['request'].user

        if business_user == reviewer:
            raise serializers.ValidationError("You cannot review yourself.")

        if Review.objects.filter(business_user=business_user, reviewer=reviewer).exists():
            raise serializers.ValidationError(
                "You have already left a review for this user."
            )
        return data

    def update(self, instance, validated_data):
        validated_data.pop('business_user', None)
        validated_data.pop('reviewer', None)
        return super().update(instance, validated_data)
