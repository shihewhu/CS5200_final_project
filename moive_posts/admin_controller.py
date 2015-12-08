from .models import EditorRequest
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage

def satisfy_all_requests():
    all_requests = EditorRequest.objects.all()
    for request in all_requests:
        editors = Group.objects.get(name="editor")
        editors.user_set.add(request.user)
        editors.save()
        request.delete()



def satisfy_one_request(request):
    editors = Group.objects.get(name="editor")
    editors.user_set.add(request.user)
    editors.save()
    email = EmailMessage('result about your request to be an editor',
                         'Congratulations, You are an editor now!',
                         to=[request.user.email])
    email.send()
    request.delete()
