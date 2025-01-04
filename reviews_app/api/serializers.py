from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from reviews_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    business_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all())
    reviewer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating',
                  'description', 'created_at', 'updated_at']
        read_only_fields = ['business_user', 'reviewer']

    def validate(self, data):
        # Ensure the user can only review the same business user once
        business_user = data.get('business_user')
        reviewer = data.get('reviewer')
        if Review.objects.filter(business_user=business_user, reviewer=reviewer).exists():
            raise serializers.ValidationError(
                "You can only leave one review per business user.")
        return data

    def update(self, instance, validated_data):
        validated_data.pop('business_user', None)
        validated_data.pop('reviewer', None)
        return super().update(instance, validated_data)
