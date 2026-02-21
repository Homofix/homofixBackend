from django.core.management.base import BaseCommand
from homofix_app.models import Customer, Booking, Technician, RechargeHistory, Task
from homofix_app.sheet_sync import (
    sync_customer, 
    sync_assigned_booking, 
    sync_completed_booking, 
    sync_cancelled_booking, 
    sync_technician, 
    sync_recharge
)
import time

class Command(BaseCommand):
    help = 'Syncs all past data to Google Sheets'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting full sync to Google Sheets...")

        # 1. Customers
        customers = Customer.objects.all()
        self.stdout.write(f"Syncing {customers.count()} Customers...")
        for customer in customers:
            try:
                sync_customer(customer)
                time.sleep(2.0) # Avoid rate limits
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error syncing Customer {customer.id}: {e}"))

        # 2. Technicians
        technicians = Technician.objects.all()
        self.stdout.write(f"Syncing {technicians.count()} Technicians...")
        for tech in technicians:
             try:
                sync_technician(tech)
                time.sleep(2.0)
             except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error syncing Technician {tech.id}: {e}"))

        # 3. Bookings (Assigned, Completed, Cancelled)
        bookings = Booking.objects.all()
        self.stdout.write(f"Syncing {bookings.count()} Bookings...")
        for booking in bookings:
            try:
                # Check for 'Assigned Bookings' tab
                # We need to see if it was ever assigned. 
                # Logic: If it has a Task, it was assigned.
                task = Task.objects.filter(booking=booking).order_by('-created_at').first()
                if task:
                    sync_assigned_booking(booking, technician=task.technician)
                    time.sleep(2.0)

                if booking.status == 'Completed':
                    sync_completed_booking(booking)
                    time.sleep(2.0)
                elif booking.status == 'Cancelled':
                    sync_cancelled_booking(booking)
                    time.sleep(2.0)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error syncing Booking {booking.id}: {e}"))

        # 4. Recharge History
        recharges = RechargeHistory.objects.all()
        self.stdout.write(f"Syncing {recharges.count()} Recharges...")
        for recharge in recharges:
             try:
                sync_recharge(recharge)
                time.sleep(2.0)
             except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error syncing Recharge {recharge.id}: {e}"))

        self.stdout.write(self.style.SUCCESS("Full sync completed!"))
