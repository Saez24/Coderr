from rest_framework import permissions, generics, filters
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from .permissions import IsCustomerProfile, IsReviewerOrAdmin
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ReviewSerializer
from reviews_app.models import Review
from rest_framework.exceptions import ValidationError
from profile_app.models import Profile
from rest_framework.permissions import IsAuthenticated, AllowAny


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business_user', 'reviewer']
    ordering_fields = ['updated_at', 'rating']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsCustomerProfile()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = Review.objects.all()
        reviewer_id = self.request.query_params.get('reviewer_id')
        business_user_id = self.request.query_params.get('business_user_id')

        if reviewer_id:
            try:
                reviewer_id = int(reviewer_id)
                queryset = queryset.filter(reviewer=reviewer_id)
            except ValueError:
                raise ValidationError(
                    "Der Parameter 'reviewer_id' muss eine Zahl sein.")

        if business_user_id:
            try:
                business_user_id = int(business_user_id)
                queryset = queryset.filter(business_user=business_user_id)
            except ValueError:
                raise ValidationError(
                    "Der Parameter 'business_user_id' muss eine Zahl sein.")

        return queryset

    def perform_create(self, serializer):
        # Setze den aktuellen User als Reviewer
        reviewer = self.request.user
        # Extrahiere die ID von `business_user`, falls ein Objekt übergeben wird
        business_user = serializer.validated_data.get('business_user')

        if isinstance(business_user, dict):
            business_user = business_user.get('pk')

        if not business_user:
            raise ValidationError(
                "Das Feld 'business_user' ist erforderlich und muss eine ID enthalten.")

        serializer.save(reviewer=self.request.user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            permission_classes = [IsAuthenticated, IsReviewerOrAdmin]
        return [permission() for permission in permission_classes]

    def partial_update(self, request, *args, **kwargs):
        self.kwargs['partial'] = True
        review = self.get_object()
        reviewer = review.reviewer
        business_user = review.business_user
        serializer = self.get_serializer(
            review, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(reviewer=reviewer, business_user=business_user)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        request = self.get_object()
        request.delete()
        return Response(status=HTTP_204_NO_CONTENT)
