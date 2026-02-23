from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Customer, Booking, Technician, RechargeHistory, Task, Wallet, BookingProduct
from .sheet_sync import (
    sync_customer, 
    sync_assigned_booking, 
    sync_completed_booking, 
    sync_cancelled_booking, 
    sync_new_booking,
    sync_technician, 
    sync_recharge
)

@receiver(post_save, sender=Customer)
def sync_customer_to_sheet(sender, instance, created, **kwargs):
    # Trigger on both create and update
    sync_customer(instance)

@receiver(post_save, sender=Task)
def sync_assigned_booking_to_sheet(sender, instance, created, **kwargs):
    # Trigger when a Task is created (Technician Assigned) or updated (e.g. Reassigned)
    sync_assigned_booking(instance.booking, technician=instance.technician)

@receiver(post_save, sender=Booking)
def sync_booking_status_change_to_sheet(sender, instance, created, **kwargs):
    if created:
        sync_new_booking(instance)
    elif instance.status == 'Completed':
        sync_completed_booking(instance)
    elif instance.status == 'Cancelled':
        sync_cancelled_booking(instance)

@receiver(post_save, sender=Technician)
def sync_expert_to_sheet(sender, instance, created, **kwargs):
    # Trigger on both create and update for experts
    sync_technician(instance)

@receiver(post_save, sender=Wallet)
def sync_wallet_to_sheet(sender, instance, created, **kwargs):
    # Sync the technician's row whenever their wallet balance is updated
    if instance.technician_id:
        sync_technician(instance.technician_id)

@receiver(post_save, sender=RechargeHistory)
def sync_recharge_to_sheet(sender, instance, created, **kwargs):
    if created:
        sync_recharge(instance)

@receiver(post_save, sender=BookingProduct)
def sync_bookingproduct_to_sheet(sender, instance, created, **kwargs):
    # When a product is added to a new booking, we sync the booking again
    # so that the Google Sheet row is updated with the product name and amounts.
    if instance.booking and instance.booking.status == 'New':
        sync_new_booking(instance.booking)