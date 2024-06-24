from django.db import models

class TextImage(models.Model):
    
    image = models.ImageField(upload_to='uploads/')  # Adjust upload_to path if needed
