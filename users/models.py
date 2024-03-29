from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=10)

    def __str__(self):       
        return self.user.username

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