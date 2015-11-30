from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect

from .models import Post
from .form import PostForm
# Create your views here.
def index(request):
    post_list = Post.objects.order_by('-rate')
    comment_set_by_post = {}
    for post in post_list:
        comment_set_by_post[post] = post.comment_set.all()
    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'top_rate_list': post_list,
        'comment_set_by_post': comment_set_by_post
    })
    return HttpResponse(template.render(context))

'''test for a post view'''
def post(request, post_num="1"):

    post = Post.objects.get(id=post_num)
    comment_set = post.comment_set.all()
    posters = post.poster_set.all()
    template = loader.get_template('post.html')
    context = RequestContext(request, {
        'post': post,
        'posters': posters,
        'comments': comment_set
    })
    return HttpResponse(template.render(context))

'''test for a forms view'''
def get_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # process data
            new_post = Post.objects.create()
            new_post.title = form.title
            new_post.release_date = form.release_date
            return HttpResponseRedirect('/thanks/')
    else:
        form = PostForm()
    return render(request, 'postform.html', {'form',form})