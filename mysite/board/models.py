# Create your models here.
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.mixins import FieldCacheMixin
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='posts')
    date_posted = models.DateTimeField('date_posted', auto_now=True)
    
    def __str__(self):
        return '{} says {}'.format(self.user.username, self.content)

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.content[:50]

class Follow(models.Model):
    user_from = models.ForeignKey(User, on_delete=CASCADE, related_name='following')
    user_to = models.ForeignKey(User, on_delete=CASCADE, related_name='followers')

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)