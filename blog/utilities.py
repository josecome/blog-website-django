from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect


class app_notifications:
    def send_email(request):
        subject = 'Password successfully changed'
        message = 'Password successfully changed for ' + request.POST['username'] + '. If is not you, change you password please!'
        from_email = 'admin@admin.com'
        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, ['admin@admin.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('login.html')
        else:
            return HttpResponse('All fields must be filled!')