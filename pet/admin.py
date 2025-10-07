from django.contrib import admin
from pet.models import Pet, Category, PetImage, Review

# Register your models here.

admin.site.register(Pet)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(PetImage)
