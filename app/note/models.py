from email.quoprimime import body_check
from django.db import models

# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=120)
    body  = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=100)


    def __str__(self):
        return '{}'.format(self.title)

    @property
    def first_five_letter_title(self):
        first_five_chars = self.title[0:5]
        return first_five_chars

