from rest_framework_nested import routers
from django.urls import path, include
from cms.views import ConferenceDetailViewSet,HeroViewSet,ConferenceViewSet,HeroInfoCardViewSet,WelComeViewset, ThemeHighlightsViewset, ScopeAreaViewset,KeynoteSpeakerViewSet,CommitteeGroupViewSet,CommitteeMemberViewSet,ArchiveLinkViewSet,ArchiveViewSet,AboutEventViewSet, HeroHighlightViewSet,VenueInfoViewSet,IndexingTargetViewSet,SponsorViewSet,ImportantDateDisplayViewSet,RegistrationFeeViewSet,ContactViewSet,ConfereneRestoreViewSet
from conferences.views import TrackViewSet,SessionViewSet,TrackRestoreViewSet, SessionRestoreViewSet
from papers.views import *


router = routers.DefaultRouter()
router.register(r'conference-details', ConferenceDetailViewSet, basename='conference-details')
router.register('conferences',ConferenceViewSet,basename='conference')
router.register('conference-restore',ConfereneRestoreViewSet, basename='conference-restore')
router.register('paper-restore',PaperRestoreViewSet,basename='paper-restore')
router.register('co-auther-restore',CoAutorRestoreViewSet,basename='coauthor-restore')
router.register('reviewer-restore', ReviewAssignmentRestoreViewSet, basename='reviewer')
router.register('review-store',ReviewRestoreViewSet, basename='review-restore')
router.register('track-restore',TrackRestoreViewSet, basename='track-restore')
router.register('session-restore',SessionRestoreViewSet,basename='session-restore')



# conference nested
conference_nested = routers.NestedDefaultRouter(router,'conferences', lookup='conference')
conference_nested.register('hero', HeroViewSet, basename='hero')
conference_nested.register('welcome', WelComeViewset, basename='welcome')
conference_nested.register('keynote',KeynoteSpeakerViewSet,basename='keynote')
conference_nested.register('committee-group', CommitteeGroupViewSet, basename='committee-group')
conference_nested.register('archive', ArchiveViewSet, basename='archive')
conference_nested.register('about-event',AboutEventViewSet,basename='aboutevent')
conference_nested.register('important-date',ImportantDateDisplayViewSet,basename='dates')
conference_nested.register('registration-fees',RegistrationFeeViewSet, basename='fees')
conference_nested.register('contact-info',ContactViewSet,basename='contact-info')
conference_nested.register('track',TrackViewSet, basename='track')


# welcome nested
welcome_nested = routers.NestedDefaultRouter(conference_nested, 'welcome', lookup='welcome')
welcome_nested.register('theme-highlight', ThemeHighlightsViewset, basename='themehighlight')
welcome_nested.register('scope-area', ScopeAreaViewset, basename='scope-area')


# hero nested for herocard info
hero_nested = routers.NestedDefaultRouter(conference_nested, 'hero', lookup='hero')
hero_nested.register('hero-info',HeroInfoCardViewSet, basename='infocard')

# committee group nested
group_nested = routers.NestedDefaultRouter(conference_nested,'committee-group', lookup='group')
group_nested.register('group-member',CommitteeMemberViewSet,basename='member')

# archive nested 
archive_nested = routers.NestedDefaultRouter(conference_nested, 'archive', lookup='archive')
archive_nested.register('archive-links',ArchiveLinkViewSet, basename='links')

# about-event nested
event_nested = routers.NestedDefaultRouter(conference_nested,'about-event', lookup='event')
event_nested.register('herohighlights',HeroHighlightViewSet, basename='hero-highlight')
event_nested.register('venue-item',VenueInfoViewSet, basename='venu')
event_nested.register('indexing-target',IndexingTargetViewSet, basename='index')
event_nested.register('sponsor',SponsorViewSet, basename='sponsor')

# track nested 
track_nested = routers.NestedDefaultRouter(conference_nested,'track',lookup='track')
track_nested.register('session',SessionViewSet, basename='session')
track_nested.register('papers', PaperViewSet,basename='paper')

# paper nested
paper_nested = routers.NestedDefaultRouter(track_nested, 'papers', lookup='paper')
paper_nested.register('status-update', PaperStatusUpdateViewSet, basename='status')
paper_nested.register('co-author',CoAuthorViewSet, basename='co-author')
paper_nested.register('review-assign',  ReviewAssignmentViewSet, basename='review-assign')


# review nested
review_nested = routers.NestedDefaultRouter(paper_nested, 'review-assign', lookup='assignment')
review_nested.register('reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('',include(router.urls)),
    path('',include(conference_nested.urls)),
    path('',include(hero_nested.urls)),
    path('',include(welcome_nested.urls)),
    path('',include(group_nested.urls)),
    path('',include(archive_nested.urls)),
    path('',include(event_nested.urls)),
    path('',include(track_nested.urls)),
    path('',include(paper_nested.urls)),
    path('',include(review_nested.urls))

]
