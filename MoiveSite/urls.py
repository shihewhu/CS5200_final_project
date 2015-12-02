"""MoiveSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from moive_posts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^homepage/$', views.homepage),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^post/(?P<func>[a-z]+)/(?P<post_num>[0-9]+)/$', views.post, name='post-func'),
    url(r'^thanks/(?P<type>[a-z]+)/(?P<post_num>[0-9]+)/$', views.thanks),
    url(r'^create/$', views.create_post),
    url(r'^edit/(?P<post_num>[0-9]+)/$', views.edit_post),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'registration/login.html',
                                                 'redirect_field_name': '/homepage/'}),
    url(r'^accounts/logout_then_login/$', auth_views.logout_then_login, {'login_url': '/accounts/login/'}),
    url(r'^accounts/profile/$', views.profile),
    url(r'^errors/(?P<type>[a-z]+)/$', views.errors),
    url(r'^accounts/increase_privilege/$', views.increase_privilege),
    url(r'^accounts/decrease_privilege/$', views.decrease_privilege),
    url(r'^success/(?P<type>[a-z]+)/$', views.success)
]

