
from conferences.models import Track,Session
from conferences.serializers import TrackSerializer,SessionSerializer
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

class SoftDeleteMixin:
    """Reusable mixin for soft delete & restore"""

    def perform_destroy(self, instance):
        """Soft delete instead of hard delete"""
        user = getattr(self.request, 'user', None)
        if user and user.is_authenticated:
            instance.delete(user=user)
        else:
            instance.delete()

    def destroy(self, request, *args, **kwargs):
        """Override default destroy response"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Soft deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )



class SoftDeleteRestoreMixin:
    @action(detail=True, methods=['get','post'])
    def restore(self, request, *args, **kwargs):
        """Restore a soft-deleted object"""
        instance = self.get_object()

        if instance.is_deleted:
            instance.restore()
            return Response(
                {"status": "restored"},
                status=status.HTTP_200_OK
            )

        return Response(
            {"status": "already_active"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['get','delete'])
    def hard_delete(self, request, slug=None):
        """Harddelete only admin user"""
        instance = self.get_object()

        if instance.products.exists():
            return Response(
                {"error": "Cannot delete category with products"},
                status=400
            )
        instance.hard_delete()
        return Response({"message": "Permanently deleted"})





class TrackViewSet(SoftDeleteMixin,ModelViewSet):
    """
    Each user can have only one track per conference
    """
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        qs = Track.objects.select_related('conference', 'user').all()

        if not user.is_authenticated:
            return qs.none()   # or raise PermissionDenied
        
        if user.role == 'admin':
            return qs

        return qs.filter(user=user)  # 

    def perform_create(self, serializer):
        user = self.request.user
        conference_id = self.kwargs.get('conference_pk')

        #  prevent DB crash (important)
        if Track.objects.filter(user=user, conference_id=conference_id).exists():
            raise ValidationError(
                "You already created a track in this conference."
            )

        serializer.save(
            conference_id=conference_id,
            user=user
        )
    
class TrackRestoreViewSet(SoftDeleteRestoreMixin,ModelViewSet):

    http_method_names = ['post']
    serializer_class = TrackSerializer
    queryset  = Track.deleted_objects.all()


class SessionViewSet(SoftDeleteMixin,ModelViewSet):
    """session created"""
    queryset = Session.objects.select_related('track').all()
    serializer_class = SessionSerializer


    def perform_create(self, serializer):
        serializer.save(track_id = self.kwargs.get('track_pk'),user = self.request.user)
    
class SessionRestoreViewSet(SoftDeleteRestoreMixin,ModelViewSet):

    http_method_names = ['post']
    serializer_class = SessionSerializer
    queryset  = Session.deleted_objects.all()