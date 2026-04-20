from core.models import BaseModel
from conferences.models import Conference
from django.db import models

class HeroSection(BaseModel):
    conference = models.OneToOneField(Conference, on_delete=models.CASCADE,related_name='hero')

    eyebrow = models.CharField(max_length=255)
    pretitle = models.CharField(max_length=255)
    title = models.TextField()

    date_line = models.CharField(max_length=255)
    summary = models.TextField(null=True,blank=True)

    cta_primary_label = models.CharField(max_length=100,blank=True)
    cta_primary_link = models.CharField(max_length=255,blank=True)

    cta_secondary_label = models.CharField(max_length=100,blank=True)
    cta_secondary_link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title

class HeroInfoCard(BaseModel):
    hero = models.ForeignKey(HeroSection, on_delete=models.CASCADE, related_name="info_cards")

    label = models.CharField(max_length=100)
    text = models.TextField(null=True,blank=True)

    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']



class WelcomeSection(BaseModel):
    conference = models.OneToOneField(
        Conference,
        on_delete=models.CASCADE,
        related_name='welcome'
    )
    heading = models.CharField(max_length=255)
    conference_name = models.TextField()

    theme_title = models.CharField(max_length=255)
    theme_intro = models.TextField()

    scope_title = models.CharField(max_length=255)
    abstract_note_title = models.CharField(max_length=255)
    abstract_note = models.TextField()

    def __str__(self):
        return self.heading
    

class ThemeHighlight(BaseModel):
    welcome = models.ForeignKey(
        WelcomeSection,
        on_delete=models.CASCADE,
        related_name="highlights"
    )
    text = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']


class ScopeArea(BaseModel):
    welcome = models.ForeignKey(
        WelcomeSection,
        on_delete=models.CASCADE,
        related_name="scopes"
    )
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return f'scope name of {self.name}'

class KeynoteSpeaker(BaseModel):
    conference = models.ForeignKey(  
		Conference,  
		on_delete=models.CASCADE,  
		related_name='keynote_speakers'  
	)

    name = models.CharField(max_length=255, db_index=True)
    title = models.CharField(max_length=255)
    affiliation = models.TextField()

    image = models.ImageField(upload_to='keynotes/',blank=True, null=True)
    profile_url = models.URLField(blank=True)
    profileLabel = models.CharField(max_length=30, default='profile')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'Keynotes for {self.name}'


class CommitteeGroup(BaseModel):
    conference = models.ForeignKey(  
		Conference,  
		on_delete=models.CASCADE,  
		related_name='committee_groups'  
	)

    title = models.CharField(max_length=255)

    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
    
    def __str__(self):
        return f'Conference commete name is {self.title}'
    


class CommitteeMember(BaseModel):
    group = models.ForeignKey(
        CommitteeGroup,
        on_delete=models.CASCADE,
        related_name="members"
    )

    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255, blank=True)
    affiliation = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    image = models.ImageField(upload_to='committee/', blank=True, null=True)

    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.group} memers is {self.name}'
    

class Archive(BaseModel):
    conference = models.ForeignKey(
        Conference,
        on_delete=models.CASCADE,
        related_name='archives'
    )

    year = models.PositiveIntegerField(db_index=True)
    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='archives/')

    class Meta:
        ordering = ['-year']
    
    def __str__(self):
        return self.title


class ArchiveLink(BaseModel):
    archive = models.ForeignKey(Archive, on_delete=models.CASCADE, related_name="links")

    label = models.CharField(max_length=100, blank='True')
    url = models.URLField()


    def __str__(self):
        return self.label
    

    class Meta:
	    unique_together = ('archive', 'url')
    
    

class AboutEvent(BaseModel):
    conference = models.OneToOneField(
        Conference,
        on_delete=models.CASCADE,
        related_name='about_event'
    )

    # Hero
    hero_badge = models.CharField(max_length=100)
    hero_title = models.CharField(max_length=255, db_index=True)
    hero_summary = models.TextField(null=True, blank=True)

    # Titles
    submission_process_title = models.CharField(max_length=255, blank=True)
    full_paper_title = models.CharField(max_length=255, blank=True)
    proceedings_title = models.CharField(max_length=255, blank=True)

    venue_title = models.CharField(max_length=255, blank=True)

    submission_path_title = models.CharField(max_length=255, blank=True)
    where_to_submit_title = models.CharField(max_length=255, blank=True)

    indexing_title = models.CharField(max_length=255, blank=True)
    indexing_disclaimer = models.TextField(blank=True)

    sponsors_title = models.CharField(max_length=255, blank=True)
    sponsors_disclaimer = models.TextField(blank=True)

    timeline_title = models.CharField(max_length=255, blank=True)

    fees_title = models.CharField(max_length=255, blank=True)
    fees_summary = models.TextField(blank=True)

    contact_title = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.hero_title
    

class HeroHighlight(models.Model):
    about_event = models.ForeignKey(
        'AboutEvent',
        on_delete=models.CASCADE,
        related_name='herohighlights'
    )

    title = models.CharField(max_length=100)
    text = models.TextField()

    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        indexes = [
            models.Index(fields=['about_event', 'order']),
        ]

    def __str__(self):
        return f"{self.title} - {self.about_event}"


class TextItem(BaseModel):

    SECTION_CHOICES = (
        ('submission', 'Submission'),
        ('full_paper', 'Full Paper'),
        ('proceedings', 'Proceedings'),
    )

    about = models.ForeignKey(
        AboutEvent,
        on_delete=models.CASCADE,
        related_name="text_items"
    )

    section = models.CharField(
        max_length=100,
        choices=SECTION_CHOICES,
        db_index=True
    )

    text = models.TextField()

    def __str__(self):
        return self.section




class VenueInfo(BaseModel):
    about = models.ForeignKey(AboutEvent, on_delete=models.CASCADE, related_name="venues")

    label = models.CharField(max_length=100)
    value = models.TextField()
    
    class Meta:
        ordering = ['created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['about', 'label'],
                name='unique_venue_label_per_about'
            )
        ]


class IndexingTarget(BaseModel):
    about = models.ForeignKey(AboutEvent, on_delete=models.CASCADE, related_name="indexings")

    label = models.CharField(max_length=255)
    image = models.ImageField(upload_to='indexing/')
    class Meta:
	    constraints = [
	        models.UniqueConstraint(
	            fields=['about', 'label'],
	            name='unique_indexing_label_per_about'
	        )
	    ]



class Sponsor(BaseModel):
    about = models.ForeignKey(AboutEvent, on_delete=models.CASCADE, related_name="sponsors")

    label = models.CharField(max_length=255)
    image = models.ImageField(upload_to='sponsors/',null=True, blank=True)
    class Meta:
	    constraints = [
	        models.UniqueConstraint(
	            fields=['about', 'label'],
	            name='unique_sponsor_per_about'
	        )
	    ]


class ImportantDate(BaseModel):
    conference = models.ForeignKey(
	    Conference,
	    on_delete=models.CASCADE,
	    related_name='important_dates'
	)

    title = models.CharField(max_length=255)
    date = models.DateField(db_index=True)
    class Meta:
	    ordering = ['-date']

class RegistrationFee(BaseModel):

    CURRENCY_CHOICES = (
        ('USD', 'USD'),
        ('BDT', 'BDT'),
        ('EUR', 'EUR'),
    )

    conference = models.ForeignKey(
        Conference,
        on_delete=models.CASCADE,
        related_name='registration_fees'
    )

    category = models.CharField(max_length=255, db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)

    class Meta:
        ordering = ['amount']
        constraints = [
            models.UniqueConstraint(
                fields=['conference', 'category'],
                name='unique_fee_category_per_conference'
            )
        ]

class ContactInfo(BaseModel):
    conference = models.OneToOneField(
	    Conference,
	    on_delete=models.CASCADE,
	    related_name='contact_info'
	)

    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)

    phone = models.CharField(max_length=100, blank=True)
    cell = models.CharField(max_length=100, blank=True)
    cta_label = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.email
    
class SubmissionConfig(BaseModel):
    conference = models.OneToOneField(
        Conference,
        on_delete=models.CASCADE,
        related_name='submission_config'
    )

    abstract_limit = models.PositiveIntegerField()
    paper_limit = models.PositiveIntegerField()

    REVIEW_CHOICES = (
        ('single_blind', 'Single Blind'),
        ('double_blind', 'Double Blind'),
        ('open', 'Open Review'),
    )
    review_type = models.CharField(max_length=20, choices=REVIEW_CHOICES)

    LANGUAGE_CHOICES = (
        ('en', 'English'),
        ('bn', 'Bengali'),
    )
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)

