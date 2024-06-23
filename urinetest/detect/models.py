from django.db import models

class TextImage(models.Model):
    text = models.CharField(max_length=255)
    image = models.ImageField(upload_to='uploads/')  # Adjust upload_to path if needed
