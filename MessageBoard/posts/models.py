from cgitb import text
from django.db import models

class Post(models.Model):
    text = models.TextField()
    
    def __str__(self) -> str:
        return self.text[0:50]
