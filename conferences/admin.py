from django.contrib import admin
from conferences.models import *
from cms.models import Conference
# Register your models here.

admin.site.register(Conference)
admin.site.register(Track)
admin.site.register(Session)

