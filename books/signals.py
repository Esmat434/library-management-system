from django.db.models.signals import post_save
from django.dispatch import receiver

from .email import send_notification_email

from .models import (
    BorrowTransaction,Reservation
)

@receiver(post_save, sender=BorrowTransaction)
def send_borrow_transaction_notification(sender,created,instance,**kwargs):
    if created:
        send_notification_email(
            instance.user.email,
            'Borrow Notification',
            instance.book_copy.book.title,
            instance.user.username
        )

@receiver(post_save, sender=Reservation)
def send_reserved_notification(sender,created,instance,**kwargs):
    if created:
        send_notification_email(
            instance.user.email,
            'Reserved Book Notication',
            instance.book_copy.book.title,
            instance.user.username
        )
