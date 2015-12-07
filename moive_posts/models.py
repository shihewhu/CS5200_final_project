from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.timezone import now
# Create your models here.
categroy_map = {
        '1': 'biography',
        '2': 'agriculture',
        '3': 'crime',
        '4': 'arts',
        '5': 'energy',
        '6': 'sports',
        '7': 'science',
        '8': 'history'
}
class Post(models.Model):
    title = models.CharField(max_length=200)
    release_date = models.DateField()
    director_name = models.CharField(max_length=200)
    cast = models.CharField(max_length=200)
    CATEGORY_CHOICES = (
        ('1', 'biography'),
        ('2', 'agriculture'),
        ('3', 'crime'),
        ('4', 'arts'),
        ('5', 'energy'),
        ('6', 'sports'),
        ('7', 'science'),
        ('8', 'history')
    )
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=4000)
    rate = models.FloatField(null=True, blank=True)
    rate_num = models.IntegerField(default=0)
    production_company = models.CharField(max_length=200)
    release_region = models.CharField(max_length=200)
    author = models.ForeignKey(User, related_name='author_name')
    comments = models.ManyToManyField(User, verbose_name='list of user', through='Comment')
    '''method'''

    def add_rate(self, rate_added):
        if self.rate_num == 0:
            self.rate = rate_added
            self.rate_num = 1
        else:
            self.rate = (self.rate * self.rate_num + rate_added) / (self.rate_num + 1)
            self.rate_num += 1
        self.save()

    def get_category(self):
        return categroy_map[self.category]

    def __str__(self):
        return self.title

    def get_absolute_view_url(self):
        return reverse('post-func', args=['view', self.id])

    def get_absolute_comment_url(self):
        return reverse('post-func', args=['comment', self.id])

    def get_absolute_rate_url(self):
        return reverse('post-func', args=['rate', self.id])


class Poster(models.Model):
    image = models.ImageField(upload_to="static/")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_content = models.CharField(max_length=4000)
    date_posted = models.DateField()
    comment_to = models.ForeignKey(Post, on_delete=models.CASCADE)
    commented_by = models.ForeignKey(User)

    def __str__(self):
        return self.comment_content


class EditorRequest(models.Model):
    """
    model for editor request
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateField(default=now)