from django.db import models

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
