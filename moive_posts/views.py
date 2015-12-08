from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import make_password
from django.core.mail import EmailMessage
from .models import EditorRequest
from .models import Post
from .models import Poster
from .models import Comment
from .form import CommentForm
from .form import PosterForm
from .form import PostForm
from .form import RateForm
from .form import UserForm
import datetime

poster_forms = []
# Create your views here.
def homepage(request):
    posts = Post.objects.all().order_by('-rate')
    if len(posts) >= 10:
        posts = posts[:10]
    return render(request, 'homepage.html', {'posts': posts,
                                             'user': request.user})


def register(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user_name = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            password_confirm = user_form.cleaned_data['password_confirm']
            if password_not_match(password, password_confirm):
                return HttpResponseRedirect('/errors/pwdnotmatch/')
            user_form.save()
            user = User.objects.get(username=user_name)
            user.password = make_password(user_form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect('/homepage/')
    else:
        user_form = UserForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


def password_not_match(password, password_confirm):
    return password_confirm != password

@login_required(login_url='/accounts/login')
def profile(request):
    post_list = Post.objects.filter(author=request.user)
    # template = loader.get_template('/registration')
    editors = Group.objects.get(name="editor")
    is_editor = request.user in editors.user_set.all()
    return render(request, 'registration/profile.html',
                  {'user': request.user,
                   'post_list': post_list,
                   'is_editor': is_editor})


@login_required(login_url='/accounts/login')
def settings(request):
    editors = Group.objects.get(name="editor")
    is_editor = request.user in editors.user_set.all()
    return render(request, 'registration/settings.html', {'user': request.user,
                                                          'is_editor': is_editor})


# need test
@login_required(login_url='/accounts/login')
def increase_privilege(request):
    editor_request = EditorRequest(user=request.user)
    editor_request.save()
    return HttpResponseRedirect('/success/editorrequest/')


@login_required(login_url='/accounts/login')
def decrease_privilege(request):
    group = Group.objects.get(name="editor")
    group.user_set.remove(request.user)
    email = EmailMessage('result about your request to cancel your editor privilege',
                         'You canceling request is successful',
                         to=[request.user.email])
    email.send()
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
def create_post(request, func):
    """
    view for creating a post and poster and save them into the database
    :param request: the request made by user
    :return:
    """
    if request.method == 'POST':
        new_post = Post()
        new_post.author = request.user
        post_form = PostForm(request.POST, instance=new_post, prefix="post_form")
        if post_form.is_valid():
            # process data
            post_form.save()
            post_num = new_post.id
            for i in range(len(poster_forms)):
                new_poster = Poster()
                new_poster.post = new_post
                poster_form = PosterForm(request.POST, request.FILES, instance=new_poster, prefix="poster_form"+str(i))
                if poster_form.is_valid():
                    poster_form.save()
            return HttpResponseRedirect('/thanks/upload/' + str(post_num)+'/')
    else:
        if func == "start":
            del poster_forms[:]
        #     poster_form = PosterForm(prefix="post_form"+str(len(poster_forms)))
        #     poster_forms.append(poster_form)
        # else:
        post_form = PostForm(prefix="post_form")
        poster_form = PosterForm(prefix="poster_form"+str(len(poster_forms)))
        poster_forms.append(poster_form)

    print poster_forms
    template = loader.get_template('create_post.html')
    context = RequestContext(request, {
        'post_form': post_form,
        'poster_forms': poster_forms
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


@permission_required('moive_posts.delete_post', raise_exception=True)
@login_required(login_url='/accounts/login')
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
        return HttpResponseRedirect("/success/delete/")


def thanks(request, type, post_num):
    """
    view for thanks page
    :param request: the request made by the user
    :param type: the type for the request
    :param post_num: the id of the post
    :return: http response with the template of "thanks.html"
    """
    template = loader.get_template('thanks.html')
    context = RequestContext(request, {
        'type': type,
        'post_num': post_num
    })
    return HttpResponse(template.render(context))


def search_category(request):
    cate = request.POST['cate']
    post_list = Post.objects.filter(category=cate)
    template = loader.get_template('search.html')
    context = RequestContext(request, {
        'post_list': post_list,
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
