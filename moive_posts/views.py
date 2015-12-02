from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from .models import Post
from .models import Poster
from .models import Comment
from .form import CommentForm
from .form import PosterForm
from .form import PostForm
from .form import RateForm
import datetime


# Create your views here.


# TODO
def homepage(request):
    posts = Post.objects.all().order_by('release_date')
    if len(posts) >= 10:
        posts = posts[:10]
    return render(request, 'homepage.html', {'posts': posts,
                                             'user': request.user})


# TODO
def register(request):
    pass


# TODO
@login_required(login_url='/accounts/login')
def profile(request):
    post_list = Post.objects.filter(author=request.user)
    # template = loader.get_template('/registration')
    return render(request, 'registration/profile.html',
                                        {'user': request.user
                                        ,'post_list': post_list})


# TODO
def increase_privilege(request):
    send_mail('request to be editor', 'username:'+request.user.username, request.user.email,
              User.objects.get(is_superuser=True).email)
    return HttpResponseRedirect('/success/editorrequest/')

# TODO
def decrease_privilege(request):
    group = Group.objects.get(name="editor")
    group.user_set.remove(request.user)
    return HttpResponseRedirect('/success/canceleditor/')


def post(request, func, post_num="1"):
    post = Post.objects.get(id=post_num)
    comment_set = post.comment_set.all()
    posters = post.poster_set.all()
    comment_form = CommentForm()
    rate_form = RateForm()
    if func == "comment":
        process_comment_post(request, comment_form, post_num)
        return HttpResponseRedirect('/thanks/comment/' + str(post_num) + '/')
    elif func == "rate":
        process_rate_post(request, rate_form, post_num)
        return HttpResponseRedirect('/thanks/rate/' + str(post_num) + '/')
    template = loader.get_template('post.html')
    context = RequestContext(request, {
        'post': post,
        'posters': posters,
        'comments': comment_set,
        'comment_form': comment_form,
        'post_num': post_num,
        'rate_form': rate_form
    })
    return HttpResponse(template.render(context))


def process_comment_post(request, comment_form, post_num):
    post = Post.objects.get(id=post_num)
    if request.method == "POST":
        new_comment = Comment()
        new_comment.commented_by = request.user
        new_comment.comment_to = post
        new_comment.date_posted = datetime.datetime.now()
        comment_form = CommentForm(request.POST, instance=new_comment)
        if comment_form.is_valid():
            comment_form.save()


def process_rate_post(request, rate_form, post_num):
    if request.method == "POST":
        post_to_rate = Post.objects.get(id=post_num)
        rate_form = RateForm(request.POST)
        if rate_form.is_valid() and rate_form.cleaned_data['rate'] < 5.0:
            post_to_rate.add_rate(rate_form.cleaned_data['rate'])


@permission_required('moive_posts.add_post', raise_exception=True)
@login_required(login_url='/accounts/login')
def create_post(request):
    """
    view for creating a post and poster and save them into the database
    :param request: the request made by user
    :return:
    """
    if request.method == 'POST':
        new_post = Post()

        new_post.author = request.user
        post_form = PostForm(request.POST, instance=new_post)
        if post_form.is_valid():
            # process data
            post_form.save()
            post_num = new_post.id
            new_poster = Poster()
            new_poster.post = new_post
            poster_form = PosterForm(request.POST, request.FILES, instance=new_poster)
            if poster_form.is_valid():
                poster_form.save()
                return HttpResponseRedirect('/thanks/upload/' + str(post_num))
    else:
        post_form = PostForm()
        poster_form = PosterForm()
    template = loader.get_template('create_post.html')
    context = RequestContext(request, {
        'post_form': post_form,
        'poster_form': poster_form
    })
    return HttpResponse(template.render(context))



@permission_required('moive_posts.change_post', raise_exception=True)
@login_required(login_url='/accounts/login')
def edit_post(request, post_num="1"):
    """
    view for editing post and poster and save them into the database
    :param request: the request made by the user
    :param: post_num: the id of the post
    :return: a http response
    """

    post_to_edit = Post.objects.get(id=post_num)
    if post_to_edit.author != request.user:
        return HttpResponseRedirect('/errors/notauthor/')
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
                return HttpResponseRedirect('/thanks/edit/' + str(post_num))

    template = loader.get_template('edit_post.html')
    context = RequestContext(request, {
        'post_form': post_form,
        'poster_forms': poster_forms,
        'post_num': post_num
    })
    return HttpResponse(template.render(context))


def delete_post(request, post_num="1"):
    """
    view for delete post action
    :param request: the request made by the user
    :param post_num: the id of the post
    :return: a http response
    """
    post_to_delete = Post.objects.get(id=post_num)
    if post_to_delete:
        post_to_delete.delete()



def thanks(request, type, post_num):
    """
    :param request:
    :param type:
    :param post_num:
    :return:
    """
    template = loader.get_template('thanks.html')
    context = RequestContext(request, {
        'type': type,
        'post_num': post_num
    })
    return HttpResponse(template.render(context))

def errors(request, type):
    """

    :param request:
    :param type:
    :return:
    """
    return render(request, "errors.html", {'type': type,
                                            'user': request.user})

def success(request, type):
    """

    :param request:
    :param type:
    :return:
    """
    return render(request, 'success.html', {'type': type})