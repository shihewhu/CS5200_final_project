from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect

from .models import Post
from .models import Poster
from .models import Comment
from .form import CommentForm
from .form import PosterForm
from .form import PostForm
import datetime


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
    if request.method == "POST":
        new_comment = Comment()
        new_comment.commented_by = request.user
        new_comment.comment_to = post
        new_comment.date_posted = datetime.datetime.now()
        comment_form = CommentForm(request.POST, instance=new_comment)
        if comment_form.is_valid():
            comment_form.save()
            return HttpResponseRedirect('/thanks/3/')
    else:
        comment_form = CommentForm()
    template = loader.get_template('post.html')
    context = RequestContext(request, {
        'post': post,
        'posters': posters,
        'comments': comment_set,
        'comment_form': comment_form,
        'post_num': post_num
    })
    return HttpResponse(template.render(context))




def create_post(request):
    '''
    view for creating a post and poster and save them into the database
    :param request:
    :return:
    '''
    if request.method == 'POST':
        new_post = Post()
        new_post.author = request.user
        post_form = PostForm(request.POST, instance=new_post)
        if post_form.is_valid():
            # process data
            post_form.save()
            new_poster = Poster()
            new_poster.post = new_post
            poster_form = PosterForm(request.POST, request.FILES, instance=new_poster)
            if poster_form.is_valid():
                poster_form.save()
                return HttpResponseRedirect('/thanks/')
    else:
        post_form = PostForm()
        poster_form = PosterForm()
    template = loader.get_template('create_post.html')
    context = RequestContext(request, {
        'post_form': post_form,
        'poster_form': poster_form
    })
    return HttpResponse(template.render(context))


def edit_post(request, post_num="1"):
    """
    view for editing post and poster and save them into the database
    :param post_id:
    :param request:
    :return:
    """
    post_to_edit = Post.objects.get(id=post_num)
    posters = [poster for poster in post_to_edit.poster_set.all()]
    post_form = PostForm(instance=post_to_edit)
    poster_forms = [PosterForm(instance=poster) for poster in posters]
    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post_to_edit)
        if post_form.is_valid():
            post_form.save()
            for poster in posters:
                poster_form = PosterForm(request.POST, request.FILES, instance=poster)
                if poster_form.is_valid():
                    poster_form.save()
                return HttpResponseRedirect('/thanks/')

    template = loader.get_template('edit_post.html')
    context = RequestContext(request, {
        'post_form': post_form,
        'poster_forms': poster_forms,
        'post_num': post_num
    })
    return HttpResponse(template.render(context))

def thanks(request, type_num):
    template = loader.get_template('thanks.html')
    context = RequestContext(request,{
        'type': type_num
    })
    return HttpResponse(template.render(context))
