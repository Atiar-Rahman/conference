from rest_framework import serializers
from .models import *

class HeroInfoCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroInfoCard
        fields = ['id','label', 'text','order']


    def create(self,validated_data):
        hero_id = self.context.get('hero_id')

        hero = HeroInfoCard.objects.create(
            hero_id=hero_id,
            **validated_data
        )

        return hero

class HeroSerializer(serializers.ModelSerializer):
    infoCards = HeroInfoCardSerializer(source='info_cards', many=True, read_only=True)

    class Meta:
        model = HeroSection
        fields = [
            'id',
            'conference',
            'eyebrow',
            'pretitle',
            'title',
            'date_line',
            'summary',
            'cta_primary_label',
            'cta_primary_link',
            'cta_secondary_label',
            'cta_secondary_link',
            'infoCards'
        ]
        read_only_fields = ['conference']

    def create(self,validated_data):
        conference_id = self.context.get('conference_id')

        hero = HeroSection.objects.create(
            conference_id=conference_id,
            **validated_data
        )

        return hero

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # rename keys to match JSON
        data['dateLine'] = data.pop('date_line')

        data['ctaPrimary'] = {
            "label": data.pop('cta_primary_label'),
            "href": data.pop('cta_primary_link')
        }

        data['ctaSecondary'] = {
            "label": data.pop('cta_secondary_label'),
            "href": data.pop('cta_secondary_link')
        }

        return data
    

class ThemeHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThemeHighlight
        fields = ['id','text','order']

    def create(self,validated_data):
        welcome_id = self.context.get('welcome_id')

        hero = ThemeHighlight.objects.create(
            welcome_id=welcome_id,
            **validated_data
        )

        return hero


class ScopeAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScopeArea
        fields = ['id','name']
                  
    def create(self,validated_data):
        welcome_id = self.context.get('welcome_id')

        hero = ScopeArea.objects.create(
            welcome_id=welcome_id,
            **validated_data
        )

        return hero

class WelcomeSerializer(serializers.ModelSerializer):
    themeHighlights = ThemeHighlightSerializer(source='highlights', many=True, read_only=True)
    scopeAreas = ScopeAreaSerializer(source='scopes', many=True, read_only= True)

    class Meta:
        model = WelcomeSection
        fields = [
            'id',
            'heading',
            'conference_name',
            'theme_title',
            'theme_intro',
            'themeHighlights',
            'scope_title',
            'scopeAreas',
            'abstract_note_title',
            'abstract_note'
        ]
    def create(self,validated_data):
        conference_id = self.context.get('conference_id')

        welcome = WelcomeSection.objects.create(
            conference_id=conference_id,
            **validated_data
        )

        return welcome

    def get_themeHighlights(self, obj):
        return [i.text for i in obj.highlights.all()]

    def get_scopeAreas(self, obj):
        return [i.name for i in obj.scopes.all()]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # rename keys
        data['conferenceName'] = data.pop('conference_name')
        data['themeTitle'] = data.pop('theme_title')
        data['themeIntro'] = data.pop('theme_intro')
        data['scopeTitle'] = data.pop('scope_title')
        data['abstractNoteTitle'] = data.pop('abstract_note_title')
        data['abstractNote'] = data.pop('abstract_note')

        return data
    

class KeynoteSpeakerSerializer(serializers.ModelSerializer):
    imageAlt = serializers.CharField(source='name')
    profileLabel = serializers.CharField(default="Profile")

    class Meta:
        model = KeynoteSpeaker
        fields = [
            'id',
            'name',
            'title',
            'affiliation',
            'image',
            'imageAlt',
            'profile_url',
            'profileLabel',
            'order'
        ]
        

    def create(self,validated_data):
        conference_id = self.context.get('conference_id')

        keynote = KeynoteSpeaker.objects.create(
            conference_id=conference_id,
            **validated_data
        )

        return keynote
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['profileUrl'] = data.pop('profile_url')
        return data
    

class CommitteeMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommitteeMember
        fields = ['id','name','description','affiliation','image','order']


    def create(self,validated_data):
        group_id = self.context.get('group_id')

        member = CommitteeMember.objects.create(
            group_id=group_id,
            **validated_data
        )

        return member


class CommitteeGroupSerializer(serializers.ModelSerializer):
    summary = serializers.SerializerMethodField()

    class Meta:
        model = CommitteeGroup
        fields = ['id','title','summary']

    def get_summary(self, obj):
        return [m.description for m in obj.members.all()]
    

    def create(self,validated_data):
        conference_id = self.context.get('conference_id')

        group = CommitteeGroup.objects.create(
            conference_id=conference_id,
            **validated_data
        )

        return group


class ArchiveLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchiveLink
        fields = ['id','label', 'url']


    def create(self,validated_data):
        archive_id = self.context.get('archive_id')

        group = ArchiveLink.objects.create(
            archive_id=archive_id,
            **validated_data
        )

        return group

class ArchiveSerializer(serializers.ModelSerializer):
    links = ArchiveLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Archive
        fields = ['id','year', 'title', 'description', 'cover_image', 'links']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['coverImage'] = data.pop('cover_image')
        return data
    
    def create(self,validated_data):
        conference_id = self.context.get('conference_id')

        group = Archive.objects.create(
            conference_id=conference_id,
            **validated_data
        )

        return group
    

#  Sub Serializers


class HeroHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroHighlight
        fields = ['id','title', 'text','order']


class VenueItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VenueInfo
        fields = ['id','label', 'value']


class IndexingTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexingTarget
        fields = ['id','label', 'image']


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['id','label', 'image']


class ContactSerializer(serializers.ModelSerializer):
    ctaLabel = serializers.CharField(source='cta_label')

    class Meta:
        model = ContactInfo
        fields = [
            'name',
            'role',
            'organization',
            'phone',
            'cell',
            'email',
            'ctaLabel'
        ]



class ImportantDateDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = ImportantDate
        fields = ['title', 'date']

    def to_representation(self, instance):
        return [
            instance.title,
            instance.date.strftime("%d %B, %Y")
        ]

class ImportantDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportantDate
        fields = ['id', 'conference', 'title', 'date']
        read_only_fields = ['conference']


class RegistrationFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationFee
        fields = [
            'id',
            'conference',
            'category',
            'amount',
            'currency'
        ]
        read_only_fields = ['conference']




#  Main AboutEvent Serializer


class AboutEventSerializer(serializers.ModelSerializer):

    #  FIXED sources (match related_name)
    heroHighlights = HeroHighlightSerializer(many=True, source='herohighlights',read_only=True)
    venueItems = VenueItemSerializer(many=True, source='venues', read_only=True)
    indexingTargets = IndexingTargetSerializer(many=True, source='indexings', read_only=True)
    sponsors = SponsorSerializer(many=True, read_only=True)

    #  FIXED: contact comes from conference
    contact = ContactSerializer(source='conference.contact_info', read_only=True)

    # dynamic lists
    submissionProcessItems = serializers.SerializerMethodField()
    fullPaperItems = serializers.SerializerMethodField()
    proceedingsItems = serializers.SerializerMethodField()
    submissionChannels = serializers.SerializerMethodField()
    keyDates = serializers.SerializerMethodField()
    registrationFees = serializers.SerializerMethodField()

    class Meta:
        model = AboutEvent
        fields = [
            'id',
            'hero_badge',
            'hero_title',
            'hero_summary',
            'heroHighlights',

            #  These MUST exist in model (otherwise remove them)
            'submission_process_title',
            'submissionProcessItems',

            'full_paper_title',
            'fullPaperItems',

            'proceedings_title',
            'proceedingsItems',

            'venue_title',
            'venueItems',

            'submission_path_title',
            'where_to_submit_title',
            'submissionChannels',

            'indexing_title',
            'indexingTargets',
            'indexing_disclaimer',

            'sponsors_title',
            'sponsors',
            'sponsors_disclaimer',

            'timeline_title',
            'keyDates',

            'fees_title',
            'fees_summary',
            'registrationFees',

            'contact_title',
            'contact'
        ]


    # FIXED dynamic methods


    def get_submissionProcessItems(self, obj):
        return list(
            obj.text_items.filter(section='submission')
            .values_list('text', flat=True)
        )

    def get_fullPaperItems(self, obj):
        return list(
            obj.text_items.filter(section='full_paper')
            .values_list('text', flat=True)
        )

    def get_proceedingsItems(self, obj):
        return list(
            obj.text_items.filter(section='proceedings')
            .values_list('text', flat=True)
        )

    def get_submissionChannels(self, obj):
        return list(
            obj.text_items.filter(section='channels')  #  must exist in choices
            .values_list('text', flat=True)
        )

    def get_keyDates(self, obj):
        return ImportantDateDisplaySerializer(
            obj.conference.important_dates.all(),
            many=True
        ).data

    def get_registrationFees(self, obj):
        return RegistrationFeeSerializer(
            obj.conference.registration_fees.all(),
            many=True
        ).data

    
    # CLEAN mapping (optional)
    

    def to_representation(self, instance):
        data = super().to_representation(instance)

        mapping = {
            'hero_badge': 'heroBadge',
            'hero_title': 'heroTitle',
            'hero_summary': 'heroSummary',
            'submission_process_title': 'submissionProcessTitle',
            'full_paper_title': 'fullPaperTitle',
            'proceedings_title': 'proceedingsTitle',
            'venue_title': 'venueTitle',
            'submission_path_title': 'submissionPathTitle',
            'where_to_submit_title': 'whereToSubmitTitle',
            'indexing_title': 'indexingTitle',
            'indexing_disclaimer': 'indexingDisclaimer',
            'sponsors_title': 'sponsorsTitle',
            'sponsors_disclaimer': 'sponsorsDisclaimer',
            'timeline_title': 'timelineTitle',
            'fees_title': 'feesTitle',
            'fees_summary': 'feesSummary',
            'contact_title': 'contactTitle',
        }

        for old, new in mapping.items():
            if old in data:
                data[new] = data.pop(old)

        return data

# submission info serialzier
class SubmissionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionConfig
        fields = [
            'abstract_limit',
            'paper_limit',
            'review_type',
            'language'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['abstractLimit'] = data.pop('abstract_limit')
        data['paperLimit'] = data.pop('paper_limit')
        data['reviewType'] = data.pop('review_type')

        return data


class ConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conference
        fields  = ['id','name','short_name','slug','location','start_date','end_date','description','is_published']
        read_only_fields = ['slug']


# final json serializer
class ConferenceDetailSerializer(serializers.ModelSerializer):
    hero = HeroSerializer()
    welcome = WelcomeSerializer()

    keynoteSpeakers = KeynoteSpeakerSerializer(source='keynote_speakers', many=True)
    committeeGroups = CommitteeGroupSerializer(source='committee_groups', many=True)
    archives = ArchiveSerializer( many=True)

    aboutEvent = AboutEventSerializer(source='about_event')
    submission = SubmissionInfoSerializer(source='submission_config')

    class Meta:
        model = Conference
        fields = [
            'hero',
            'welcome',
            'keynoteSpeakers',
            'committeeGroups',
            'archives',
            'aboutEvent',
            'submission'
        ]


