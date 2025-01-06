from profile_app.models import Profile
from rest_framework import permissions
from django.contrib.auth.models import User


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if Profile.objects.get(user=request.user.pk) == obj.business_user or request.user.is_staff:
            return True
        return False


class IsCustomerProfile(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and is_customer_profile(request)


def is_customer_profile(request):
    profile = Profile.objects.filter(user=request.user.pk).first()
    if profile and profile.type == "customer":
        return True
    return False
