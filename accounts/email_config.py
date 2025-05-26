from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

def send_verification_mail(to,subject,token):
    html_content = render_to_string('email.html',{'token':token})
    email = EmailMessage(subject,html_content,settings.EMAIL_HOST_USER,[to])
    email.content_subtype = 'html'

    try:
        email.send()
    except Exception as e:
        return e