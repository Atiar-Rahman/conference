from django.contrib import admin

# Register your models here.
from cms.models import *

admin.site.register(HeroSection)
admin.site.register(HeroHighlight)
admin.site.register(HeroInfoCard)
admin.site.register(WelcomeSection)
admin.site.register(ThemeHighlight)
admin.site.register(ScopeArea)
admin.site.register(KeynoteSpeaker)

admin.site.register(CommitteeGroup)
admin.site.register(CommitteeMember)

admin.site.register(Archive)
admin.site.register(ArchiveLink)
admin.site.register(AboutEvent)

admin.site.register(VenueInfo)
admin.site.register(IndexingTarget)

admin.site.register(Sponsor)

admin.site.register(ImportantDate)

admin.site.register(RegistrationFee)
admin.site.register(ContactInfo)
admin.site.register(SubmissionConfig)


