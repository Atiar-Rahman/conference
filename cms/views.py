from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from cms.serializers import ConferenceDetailSerializer, HeroSerializer,ConferenceSerializer,HeroInfoCardSerializer,WelcomeSerializer, ThemeHighlightSerializer,ScopeAreaSerializer, KeynoteSpeakerSerializer,CommitteeMemberSerializer,CommitteeGroupSerializer,ArchiveSerializer,ArchiveLinkSerializer,AboutEventSerializer,HeroHighlightSerializer,VenueItemSerializer,IndexingTargetSerializer,SponsorSerializer,ContactSerializer,ImportantDateDisplaySerializer,RegistrationFeeSerializer,ImportantDateSerializer
from conferences.models import Conference
from cms.models import HeroSection,HeroInfoCard, WelcomeSection, ThemeHighlight,ScopeArea,KeynoteSpeaker,CommitteeMember,CommitteeGroup,Archive,ArchiveLink,AboutEvent,HeroHighlight,ContactInfo, VenueInfo, IndexingTarget, Sponsor,ImportantDate,RegistrationFee

from rest_framework.permissions import IsAdminUser,IsAuthenticated
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


class ConferenceDetailViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Conference.objects.all()
    serializer_class = ConferenceDetailSerializer
    lookup_field = 'slug'

class ConferenceViewSet(SoftDeleteMixin,ModelViewSet):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer

class ConfereneRestoreViewSet(SoftDeleteRestoreMixin,ModelViewSet):

    http_method_names = ['get','post']
    serializer_class = ConferenceSerializer
    queryset  = Conference.deleted_objects.all()


class HeroViewSet(ModelViewSet):
    queryset = HeroSection.objects.all()
    serializer_class = HeroSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['conference_id'] = self.kwargs.get('conference_pk')

        return context


class HeroInfoCardViewSet(ModelViewSet):
    queryset = HeroInfoCard.objects.select_related('hero').all()
    serializer_class = HeroInfoCardSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['hero_id'] = self.kwargs.get('hero_pk')

        return context
    

class WelComeViewset(ModelViewSet):
    queryset = WelcomeSection.objects.prefetch_related('highlights','scopes')
    serializer_class = WelcomeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['conference_id'] = self.kwargs.get('conference_pk')

        return context


class ThemeHighlightsViewset(ModelViewSet):
    queryset = ThemeHighlight.objects.all()
    serializer_class = ThemeHighlightSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['welcome_id'] = self.kwargs.get('welcome_pk')

        return context

class ScopeAreaViewset(ModelViewSet):
    queryset = ScopeArea.objects.all()
    serializer_class =  ScopeAreaSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['welcome_id'] = self.kwargs.get('welcome_pk')

        return context



class KeynoteSpeakerViewSet(ModelViewSet):
    queryset = KeynoteSpeaker.objects.select_related('conference').all()
    serializer_class = KeynoteSpeakerSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['conference_id'] = self.kwargs.get('conference_pk')

        return context



class CommitteeMemberViewSet(ModelViewSet):
    queryset = CommitteeMember.objects.all()
    serializer_class = CommitteeMemberSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['group_id'] = self.kwargs.get('group_pk')

        return context

class CommitteeGroupViewSet(ModelViewSet):
    queryset = CommitteeGroup.objects.all()
    serializer_class = CommitteeGroupSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['conference_id'] = self.kwargs.get('conference_pk')

        return context
    


class ArchiveViewSet(ModelViewSet):
    queryset = Archive.objects.select_related('conference').all()
    serializer_class = ArchiveSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['conference_id'] = self.kwargs.get('conference_pk')

        return context


class ArchiveLinkViewSet(ModelViewSet):
    queryset = ArchiveLink.objects.select_related('archive').all()
    serializer_class = ArchiveLinkSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['archive_id'] = self.kwargs.get('archive_pk')

        return context
    


class AboutEventViewSet(ModelViewSet):
    serializer_class = AboutEventSerializer

    def get_queryset(self):
        conference_id = self.kwargs.get('conference_pk')

        queryset = AboutEvent.objects.select_related(
            'conference',
            'conference__contact_info'
            ).prefetch_related(
                'herohighlights',
                'venues',
                'indexings',
                'sponsors',
                'text_items',
                'conference__important_dates',
                'conference__registration_fees',
            )

        if conference_id:
            queryset = queryset.filter(conference_id=conference_id)

        return queryset
    
    def perform_create(self, serializer):
        conference_id = self.kwargs.get('conference_pk')
        serializer.save(conference_id=conference_id)



class HeroHighlightViewSet(ModelViewSet):
    queryset = HeroHighlight.objects.all()
    serializer_class= HeroHighlightSerializer

    def perform_create(self, serializer):
        serializer.save(about_event_id = self.kwargs.get('event_pk'))

class VenueInfoViewSet(ModelViewSet):
    queryset = VenueInfo.objects.all()
    serializer_class = VenueItemSerializer

    def perform_create(self, serializer):
        serializer.save(about_id = self.kwargs.get('event_pk'))

class IndexingTargetViewSet(ModelViewSet):
    queryset = IndexingTarget.objects.all()
    serializer_class = IndexingTargetSerializer

    def perform_create(self, serializer):
        serializer.save(about_id = self.kwargs.get('event_pk'))
    
class SponsorViewSet(ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer

    def perform_create(self, serializer):
        serializer.save(about_id = self.kwargs.get('event_pk'))


class ImportantDateDisplayViewSet(ModelViewSet):
    queryset = ImportantDate.objects.all()
    serializer_class = ImportantDateDisplaySerializer

    def get_serializer_class(self): 
        if self.action in ['list', 'retrieve']:
            return ImportantDateDisplaySerializer
        return ImportantDateSerializer  

    def perform_create(self, serializer):
        serializer.save(conference_id = self.kwargs.get('conference_pk'))


class RegistrationFeeViewSet(ModelViewSet):
    queryset = RegistrationFee.objects.all()
    serializer_class = RegistrationFeeSerializer

    def perform_create(self, serializer):
        serializer.save(conference_id = self.kwargs.get('conference_pk'))



class ContactViewSet(ModelViewSet):
    queryset = ContactInfo.objects.all()
    serializer_class = ContactSerializer

    def perform_create(self, serializer):
        serializer.save(conference_id = self.kwargs.get('conference_pk'))
