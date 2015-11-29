from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import Post
# Create your views here.
def index(request):
    post_list = Post.objects.order_by('rate')
    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'top_rate_list': post_list
    })
    return HttpResponse(template.render(context))