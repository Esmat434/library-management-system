from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

def send_notification_email(to,subject,instance,title):
    html_content = render_to_string('books/email.html',{'instance':instance,'subject':subject,'title':title})
    email = EmailMessage(subject,html_content,settings.EMAIL_HOST_USER,to=[to])
    email.content_subtype = 'html'

    try:
        email.send()
    except Exception as e:
        return e