from django.contrib import admin
from papers.models import *
# Register your models here.

admin.site.register(Review)
admin.site.register(ReviewAssignment)
admin.site.register(Paper)
admin.site.register(CoAuthor)

