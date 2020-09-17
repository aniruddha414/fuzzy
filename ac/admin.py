from django.contrib import admin

# Register your models here.
from ac.models import Ac,Rule

admin.site.register(Ac)
admin.site.register(Rule)