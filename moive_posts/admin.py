from django.contrib import admin
from .models import Post
from .models import Poster
from .models import Comment
# Register your models here.
admin.site.register(Post)
admin.site.register(Poster)
admin.site.register(Comment)