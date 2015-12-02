from django import forms
from django.forms import ModelForm
from models import Post
from models import Comment
from models import Poster
from django.contrib.auth.forms import AuthenticationForm



class PostForm(ModelForm):
    class Meta:
        model = Post
        field = [
            'title',
            'release_date',
            'director_name',
            'cast',
            'category',
            'description',
            'production_company',
            'release_region'
        ]
        exclude = [
            'rate',
            'rate_num',
            'author',
            'comments'
        ]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        field = [
            'comment_content'
        ]
        exclude = [
            'comment_to',
            'commented_by',
            'date_posted'
        ]


class PosterForm(ModelForm):
    class Meta:
        model = Poster
        field = [
            'image'
        ]
        exclude = [
            'post'
        ]

class RateForm(forms.Form):
    rate = forms.FloatField(required=True)