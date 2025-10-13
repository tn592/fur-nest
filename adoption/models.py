from django.db import models
from users.models import User
from pet.models import Pet
from uuid import uuid4

# Create your models here.


class Adopt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="adopt")
    adopted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Adoption {self.id} by {self.user.first_name}"


class AdoptionHistory(models.Model):
    adopt = models.ForeignKey(Adopt, on_delete=models.CASCADE, related_name="adoptions")
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.pet.name} adopted by {self.adopt.user.first_name}"


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    adoption = models.ForeignKey(
        AdoptionHistory, on_delete=models.CASCADE, related_name="payments"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=30, default="Completed")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} BDT - {self.status}"
