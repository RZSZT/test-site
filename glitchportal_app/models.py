from django.db import models

# Create your models here.
class GifModel(models.Model):
    picture = models.ImageField(upload_to = 'pictures')
    
    class Meta:
        db_table: "theGif"
                                
