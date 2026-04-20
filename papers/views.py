from rest_framework.viewsets import ModelViewSet
from papers.models import Paper,CoAuthor,Review,ReviewAssignment
from papers.serializers import PaperSerializer,PaperStatusUpdateSerializer,CoAuthorSerializer,ReviewAssignmentSerializer,ReviewSerializer
from papers.permissions import IsAdminOrReviewer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from conferences.models import Track


class SoftDeleteMixin:
    """Reusable mixin for soft delete & restore"""

    def perform_destroy(self, instance):
        """Soft delete instead of hard delete"""
        user = getattr(self.request, 'user', None)
        if user and user.is_authenticated:
            instance.soft_delete(user=user)
        else:
            instance.soft_delete()

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
        instance.delete()
        return Response({"message": "Permanently deleted"})



class PaperViewSet(SoftDeleteMixin, ModelViewSet):
    """
    Paper can be created only by authenticated user
    under a valid track with submission rules.
    """

    serializer_class = PaperSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Paper.objects.select_related('track').filter(is_deleted=False)

    def perform_create(self, serializer):
        user = self.request.user

        # 1. Safe track fetch (prevents invalid / deleted track)
        track = get_object_or_404(
            Track,
            pk=self.kwargs.get('track_pk'),
            is_deleted=False
        )

        #  2. Prevent duplicate submission (same user + same track)
        if Paper.objects.filter(
            track=track,
            author=user,
            is_deleted=False
        ).exists():
            raise ValidationError(
                "You already submitted a paper for this track."
            )

        # 3. Save paper
        serializer.save(
            track=track,
            author=user
        )

class PaperRestoreViewSet(SoftDeleteRestoreMixin,ModelViewSet):

    http_method_names = ['post']
    serializer_class = PaperSerializer
    queryset  = Paper.deleted_objects.all()


class PaperStatusUpdateViewSet(ModelViewSet):
    """permission only admin and reviewer"""
    serializer_class = PaperStatusUpdateSerializer
    http_method_names = ['get','patch']
    permission_classes = [IsAdminOrReviewer]

    def get_queryset(self):
        return Paper.objects.filter(id=self.kwargs.get('paper_pk'))



class CoAuthorViewSet(SoftDeleteMixin,ModelViewSet):
    queryset = CoAuthor.objects.select_related('paper', 'user').all()
    serializer_class = CoAuthorSerializer
    permission_classes = [IsAuthenticated]

    # auto-assign paper from URL
    def perform_create(self, serializer):
        paper = get_object_or_404(
            Paper,
            pk=self.kwargs.get("paper_pk")
        )
        serializer.save(paper=paper)

    # optional: restrict access per paper
    def get_queryset(self):
        paper_pk = self.kwargs.get("paper_pk")
        if paper_pk:
            return self.queryset.filter(paper_id=paper_pk)
        return self.queryset


class CoAutorRestoreViewSet(SoftDeleteRestoreMixin,ModelViewSet):

    http_method_names = ['post']
    serializer_class = CoAuthorSerializer
    queryset  = CoAuthor.deleted_objects.all()


class ReviewAssignmentViewSet(SoftDeleteMixin,ModelViewSet):
    queryset = ReviewAssignment.objects.select_related('paper', 'reviewer')
    serializer_class = ReviewAssignmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != "admin":
            raise PermissionDenied("Only admin can assign reviewers.")

        serializer.save()

class ReviewAssignmentRestoreViewSet(SoftDeleteRestoreMixin,ModelViewSet):

    http_method_names = ['post']
    serializer_class = ReviewAssignmentSerializer
    queryset  = ReviewAssignment.deleted_objects.all()



class ReviewViewSet(SoftDeleteMixin,ModelViewSet):
    queryset = Review.objects.select_related('assignment').all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        assignment = get_object_or_404(
             ReviewAssignment,
             pk=self.kwargs.get('assignment_pk')
        )
        

        # ensure reviewer is correct
        if assignment.reviewer != self.request.user:
            raise PermissionDenied("Not your assignment.")

        serializer.save(assignment=assignment)

    def get_serializer_context(self):
        context = super().get_serializer_context()

        if getattr(self, 'swagger_fake_view', False):
            return context
        
        assignment = get_object_or_404(
            ReviewAssignment,
            pk=self.kwargs.get('assignment_pk')
        )

        context["assignment"] = assignment
        context['request'] = self.request
        return context

class ReviewRestoreViewSet(SoftDeleteRestoreMixin,ModelViewSet):

    http_method_names = ['post']
    serializer_class = ReviewSerializer
    queryset  = Review.deleted_objects.all()