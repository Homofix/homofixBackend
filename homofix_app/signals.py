from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Booking, Share

@receiver(pre_save, sender=Booking)
def update_share_percentage(sender, instance, **kwargs):
    share = Share.objects.get(task='booking_share')
    share_percentage = share.percentage
    instance.share_percentage = share_percentage