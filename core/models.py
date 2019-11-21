from django.db import models
from django.urls import reverse
from django.utils import timezone

class Debtor(models.Model):

    name = models.CharField(max_length=50)
    amount_owed = models.FloatField()
    email = models.EmailField(max_length=254)
    is_paid = models.BooleanField(default=False)
    due_date = models.DateField(default=timezone.now)
    last_email_sent = models.DateField(null=True, blank=True)

    created_by = models.ForeignKey("users.Profile", verbose_name="Profile", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} is owed {self.amount_owed}"

    def get_absolute_url(self):
        return reverse("debtors-list")