from rest_framework.views import APIView
from rest_framework.response import Response
from profile_app.models import Profile
from .serializers import ProfileSerializer, UserSerializer
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .permissions import IsOwnerOrAdmin


class ProfileViewSets(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT']:
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get(self, request, *args, **kwargs):
        try:
            pk = self.kwargs.get('pk')
            profiles = Profile.objects.get(user=pk)
            serializer = ProfileSerializer(profiles)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NotFound:
            return Response({
                "detail": "Profile not found"
            }, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        user = User.objects.get(pk=pk)

        try:
            profile = Profile.objects.get(user=pk)
            if not (request.user == user or request.user.is_staff):
                raise PermissionDenied("Not allowed to edit this profile.")

            # Profil aktualisieren
            profile_data = self.update_profile(profile, request.data)

            # Benutzer aktualisieren
            self.update_user(user, request.data)

            return Response(profile_data, status=status.HTTP_200_OK)
        except NotFound:
            return Response({
                "detail": "Profile not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({
                "detail": "Not allowed to edit this profile."
            }, status=status.HTTP_403_FORBIDDEN)
        except ValidationError as e:
            return Response({
                "errors": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)

    def update_profile(self, profile, data):
        profile_serializer = ProfileSerializer(
            profile, data=data, partial=True)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()
        return profile_serializer.data

    def update_user(self, user, data):
        user_data = {}
        if 'first_name' in data:
            user_data['first_name'] = data['first_name']
        if 'last_name' in data:
            user_data['last_name'] = data['last_name']
        if 'email' in data:
            user_data['email'] = data['email']

        if user_data:
            user_serializer = UserSerializer(
                user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()


class ProfileCustomerViewSets(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        customer_profiles = Profile.objects.filter(type="customer")
        return_data_customer_profiles = []
        for profile in customer_profiles:
            return_data_customer_profiles.append({
                # Verwende UserSerializer
                "user": UserSerializer(profile.user).data,
                "file": profile.file.url if profile.file else None,
                "uploaded_at": profile.uploaded_at,
                "type": profile.type
            })
        return Response(return_data_customer_profiles, status=status.HTTP_200_OK)


class ProfileBusinessViewSets(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        business_profiles = Profile.objects.filter(type="business")
        return_data_business_profiles = []
        for profile in business_profiles:
            return_data_business_profiles.append({
                # Verwende UserSerializer
                "user": UserSerializer(profile.user).data,
                "file": profile.file.url if profile.file else None,
                "location": profile.location,
                "tel": profile.tel,
                "description": profile.description,
                "working_hours": profile.working_hours,
                "type": profile.type
            })
        return Response(return_data_business_profiles, status=status.HTTP_200_OK)
