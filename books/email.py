from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

def send_notification_email(to,subject,book_title,username):
    html_content = render_to_string('books/email.html',{'title':book_title,'username':username})
    email = EmailMessage(subject,html_content,settings.EMAIL_HOST_USER,to=[to])
    email.content_subtype = 'html'

    try:
        email.send()
    except Exception as e:
        return e