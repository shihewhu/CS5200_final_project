from django.contrib import admin
from .models import Post
from .models import Poster
# Register your models here.
admin.site.register(Post)
admin.site.register(Poster)