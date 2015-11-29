from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200, null=False)
    release_date = models.DateField(null=False)
    director_name = models.CharField(max_length=200, null=False)
    cast = models.CharField(max_length=200, null=False)
    CATEGORY_CHOICES = (
        ('0', 'biograhpy'),
        ('1', 'agriculture'),
        ('2', 'crime'),
        ('3', 'arts'),
        ('4', 'energy'),
        ('5', 'sports'),
        ('6', 'science'),
        ('7', 'history')
    )
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=4000)
    rate = models.FloatField(null=True, blank=True, default=0.0)
    production_company = models.CharField(max_length=200)
    release_region = models.CharField(max_length=200)
    author = models.ForeignKey(User, related_name= 'author_name')
    comments = models.ManyToManyField(User, verbose_name='list of user', through='Comment')
    ''' method'''

class Poster(models.Model):
    image = models.ImageField()
    post = models.ForeignKey(Post)

class Comment(models.Model):
    comment_content = models.CharField(max_length=4000)
    date_posted = models.DateField()
    comment_to = models.ForeignKey(Post)
    commented_by = models.ForeignKey(User)




