from django.db import models
from django.conf import settings
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = [
            "-id",
        ]

    def __str__(self):
        return self.name


class Pet(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="pets"
    )
    breed = models.CharField(max_length=200)
    age = models.PositiveIntegerField()
    description = models.TextField()
    availability = models.BooleanField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = [
            "-id",
        ]

    def __str__(self):
        return self.name


class Review(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ratings = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user.first_name} on {self.pet.name}"
