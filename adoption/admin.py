from django.contrib import admin
from adoption.models import Adopt, AdoptionHistory

# Register your models here.


# @admin.register(Adopt)
# class AdoptAdmin(admin.ModelAdmin):
#     list_display = ["id", "user"]


# @admin.register(AdoptionHistory)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ["id", "user", "status"]


# admin.site.register(Cart)
admin.site.register(Adopt)
admin.site.register(AdoptionHistory)
