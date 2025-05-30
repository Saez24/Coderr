from rest_framework import permissions
from profile_app.models import Profile


class IsReviewerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            # Überprüfen, ob der aktuelle Benutzer der Reviewer ist
            reviewer_profile = Profile.objects.get(user=request.user)

            # Überprüfen, ob der Reviewer mit dem Benutzer des Objekts übereinstimmt
            if reviewer_profile.user == obj.reviewer:
                return True

            # Überprüfen, ob der Benutzer ein Administrator ist
            if request.user.is_staff:
                return True
        except Profile.DoesNotExist:
            # Falls `obj.reviewer` oder andere Attribute nicht existieren
            return False

        return False


class IsCustomerProfile(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and is_customer_profile(request)


def is_customer_profile(request):
    profile = Profile.objects.get(user=request.user.pk)
    if profile.type == "customer":
        return True
    else:
        return False
