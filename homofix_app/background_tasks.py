from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .models import Task, Wallet, WalletHistory

def check_incomplete_bookings():
    # Get all tasks that are more than 24 hours old
    twenty_four_hours_ago = timezone.now() - timedelta(hours=48)
    incomplete_tasks = Task.objects.filter(
        booking__booking_date__lte=twenty_four_hours_ago,
        technician__isnull=False
    )

    for task in incomplete_tasks:
        # Check if the booking associated with this task is assigned but not completed
        # Only deduct money if booking status is 'Assign'
        if task.booking and task.booking.status == 'Assign' or task.booking.status == 'Reached':
            technician = task.technician
            
            # Get or create wallet for the technician
            wallet, created = Wallet.objects.get_or_create(technician_id=technician)
            
            # Create wallet history entry for penalty
            WalletHistory.objects.create(
                wallet=wallet,
                type='deduction',
                amount=Decimal('50.00'),  # Deduct 50 rupees
                description=f'Since the status of booking {task.booking.order_id} was not marked as complete within 24 hours, ₹50 has been deducted.'
            )
            
            # Deduct amount from wallet
            wallet.deduct_amount(Decimal('50.00'))