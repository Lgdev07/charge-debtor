from django.db import models
from django.urls import reverse
from django.utils import timezone
from PIL import Image


class Debtor(models.Model):

    name = models.CharField(max_length=50)
    amount_owed = models.FloatField()
    email = models.EmailField(max_length=254)
    is_paid = models.BooleanField(default=False)
    due_date = models.DateField(default=timezone.now)
    last_email_sent = models.DateField(null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='debtor_pics')

    created_by = models.ForeignKey("users.Profile", verbose_name="Created By", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} is owed {self.amount_owed}"

    def get_absolute_url(self):
        return reverse("debtors-list")
    
    def save(self, *args, **kwargs):
        """Method Inherits from Original
        to Resize Profile Image Size
        """        
        super().save(*args, **kwargs)    
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)