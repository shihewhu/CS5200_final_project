from django import forms

class PostForm(forms.Form):
    title = forms.CharField(label='title', max_length=200, required=True)
    release_date = forms.DateField(required=True, label='release date')
    director_name = forms.CharField(max_length=200, required=True, label='director')
    cast = forms.CharField(max_length=200, required=True, label='cast')
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
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=True, label='category')
    description = forms.CharField(max_length=4000, required=True, label='description')
    rate = forms.IntegerField(required=True, label='rate')
    production_company = forms.CharField(max_length=200, required=True, label='production company')
    release_region = forms.CharField(max_length=200, required=True, label='regions')
