from django.db import models

# Create your models here.
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.mixins import FieldCacheMixin
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='tweets')
    date_posted = models.DateTimeField('date_posted', auto_now=True)
    
    def __str__(self):
        return '{} says {}'.format(self.user.username, self.content)