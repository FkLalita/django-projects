from django.db import models

# Create your models here.

class Story(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    date_posted = models.DateTimeField(auto_now=True)
    content = models.TextField()
    story_pic = models.ImageField(default='image', upload_to='images/')


    def __str__(self):
        return self.title