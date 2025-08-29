from django.contrib import admin
from adoption.models import Adopt, AdoptionHistory

admin.site.register(Adopt)
admin.site.register(AdoptionHistory)
