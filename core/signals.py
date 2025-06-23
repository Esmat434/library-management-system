from django.db.models.signals import post_save
from django.dispatch import receiver

from .email import (
    send_message_email
)

from .models import (
    Contact
)

@receiver(post_save,sender=Contact)
def send_contact_message_notification(sender,created,instance,**kwargs):
    if created:
        send_message_email('Contact US',instance.title,instance.message,instance.username)
