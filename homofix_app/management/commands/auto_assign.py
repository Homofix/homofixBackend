# from django.core.management.base import BaseCommand
# from homofix_app.models import AutoAssignSetting, Technician, Booking, Task, TechnicianAssignmentTracker

# class Command(BaseCommand):
#     help = 'Auto-assign unassigned bookings if AutoAssignSetting is ON'

#     def handle(self, *args, **kwargs):
#         setting = AutoAssignSetting.objects.first()
#         if not setting or not setting.is_enabled:
#             self.stdout.write(self.style.WARNING("Auto-assign is OFF"))
#             return

#         technicians = list(Technician.objects.filter(status="Active"))
#         if not technicians:
#             self.stdout.write(self.style.ERROR("No active technicians found"))
#             return

#         # Get last technician from tracker
#         tracker, created = TechnicianAssignmentTracker.objects.get_or_create(id=1)
#         last_tech = tracker.last_assigned_technician
#         start_index = 0
#         if last_tech and last_tech in technicians:
#             last_index = technicians.index(last_tech)
#             start_index = (last_index + 1) % len(technicians)

#         new_bookings = Booking.objects.filter(status='New')
#         if not new_bookings.exists():
#             self.stdout.write(self.style.WARNING("No new bookings found"))
#             return

#         count = 0
#         for i, booking in enumerate(new_bookings):
#             technician = technicians[(start_index + i) % len(technicians)]
            
#             # Create task
#             task = Task.objects.create(booking=booking, technician=technician)
            
#             # Update booking status
#             booking.status = 'Assign'
#             booking.save()

#             # Update last assigned technician in tracker
#             tracker.last_assigned_technician = technician
#             tracker.save()

#             count += 1
#             self.stdout.write(f"✔️ Booking ID {booking.id} assigned to Technician ID {technician.id}")

#         self.stdout.write(self.style.SUCCESS(f"✅ {count} new bookings assigned and tasks created."))



# from django.core.management.base import BaseCommand
# from datetime import date
# from homofix_app.models import (
#     AutoAssignSetting, Technician, Booking, Task,
#     TechnicianAssignmentTracker, UniversalCredential,
#     Slot, Pincode
# )

# class Command(BaseCommand):
#     help = 'Auto-assign unassigned bookings if AutoAssignSetting is ON'

#     def handle(self, *args, **kwargs):
#         setting = AutoAssignSetting.objects.first()
#         if not setting or not setting.is_enabled:
#             self.stdout.write(self.style.WARNING("Auto-assign is OFF"))
#             return

#         universal_slot_obj = UniversalCredential.objects.first()
#         universal_limit = universal_slot_obj.universal_slot if universal_slot_obj else 0

#         tracker, _ = TechnicianAssignmentTracker.objects.get_or_create(id=1)

#         new_bookings = Booking.objects.filter(status='New')
#         if not new_bookings.exists():
#             self.stdout.write(self.style.WARNING("No new bookings found"))
#             return

#         total_assigned = 0

#         for booking in new_bookings:
#             # Convert zipcode (char) to Pincode object
#             # booking_pincode_obj = Pincode.objects.filter(pincode=booking.zipcode).first()
#             booking_pincode_obj = Pincode.objects.filter(code=booking.zipcode).first()

#             if not booking_pincode_obj:
#                 self.stdout.write(self.style.WARNING(f"No matching Pincode found for Booking ID {booking.id} (zipcode: {booking.zipcode})"))
#                 continue

#             # Slot limit check
            
#             slot_obj = Slot.objects.filter(pincode=booking_pincode_obj, date=date.today()).order_by('-id').first()


#             slot_limit = slot_obj.limit if slot_obj and slot_obj.limit is not None else universal_limit

#             if total_assigned >= slot_limit:
#                 self.stdout.write(self.style.WARNING(f"Slot limit reached for Pincode {booking.zipcode}"))
#                 continue

#             # Filter eligible technicians
#             eligible_techs = Technician.objects.filter(
#                 status="Active",
#                 working_pincode_areas=booking_pincode_obj
#             ).distinct()

#             if not eligible_techs.exists():
#                 self.stdout.write(self.style.WARNING(f"No technician found for Booking ID {booking.id} in Pincode {booking.zipcode}"))
#                 continue

#             tech_list = list(eligible_techs)
#             start_index = 0
#             if tracker.last_assigned_technician in tech_list:
#                 last_index = tech_list.index(tracker.last_assigned_technician)
#                 start_index = (last_index + 1) % len(tech_list)

#             technician = tech_list[start_index]

#             # Assign task
#             Task.objects.create(booking=booking, technician=technician)

#             # Update booking
#             booking.status = 'Assign'
#             booking.save()

#             # Update tracker
#             tracker.last_assigned_technician = technician
#             tracker.save()

#             total_assigned += 1
#             self.stdout.write(f"✔️ Booking ID {booking.id} assigned to Technician ID {technician.id}")

#         self.stdout.write(self.style.SUCCESS(f"✅ {total_assigned} bookings assigned based on pincodes and limits."))

from django.core.management.base import BaseCommand
from datetime import date
from homofix_app.models import (
    AutoAssignSetting, Technician, Booking, Task,
    TechnicianAssignmentTracker, UniversalCredential,
    Slot, Pincode
)

class Command(BaseCommand):
    help = 'Auto-assign unassigned bookings if AutoAssignSetting is ON'

    def handle(self, *args, **kwargs):
        setting = AutoAssignSetting.objects.first()
        if not setting or not setting.is_enabled:
            self.stdout.write(self.style.WARNING("Auto-assign is OFF"))
            return

        universal_slot_obj = UniversalCredential.objects.first()
        universal_limit = universal_slot_obj.universal_slot if universal_slot_obj else 0

        tracker, _ = TechnicianAssignmentTracker.objects.get_or_create(id=1)

        new_bookings = Booking.objects.filter(status='New')
        if not new_bookings.exists():
            self.stdout.write(self.style.WARNING("No new bookings found"))
            return

        total_assigned = 0

        for booking in new_bookings:
            booking_pincode_obj = Pincode.objects.filter(code=booking.zipcode).first()

            if not booking_pincode_obj:
                self.stdout.write(self.style.WARNING(f"No matching Pincode found for Booking ID {booking.id} (zipcode: {booking.zipcode})"))
                continue

            # Slot limit check
            slot_obj = Slot.objects.filter(pincode=booking_pincode_obj, date=date.today(),slot=booking.slot).order_by('-id').first()
            slot_limit = slot_obj.limit if slot_obj and slot_obj.limit is not None else universal_limit

            if total_assigned >= slot_limit:
                self.stdout.write(self.style.WARNING(f"Slot limit reached for Pincode {booking.zipcode}"))
                continue

            # Filter eligible technicians
            eligible_techs = Technician.objects.filter(
                status="Active",
                working_pincode_areas=booking_pincode_obj
            ).distinct()

            if not eligible_techs.exists():
                self.stdout.write(self.style.WARNING(f"No technician found for Booking ID {booking.id} in Pincode {booking.zipcode}"))
                continue

            # Prepare round robin list
            tech_list = list(eligible_techs)

            if tracker.last_assigned_technician in tech_list:
                last_index = tech_list.index(tracker.last_assigned_technician)
                tech_list = tech_list[last_index + 1:] + tech_list[:last_index + 1]

            assigned = False
            for technician in tech_list:
                task_count = Task.objects.filter(
                    technician=technician,
                    booking__status='Assign'
                ).count()

                if task_count < 4:
                    # Assign task
                    Task.objects.create(booking=booking, technician=technician)

                    # Update booking
                    booking.status = 'Assign'
                    booking.save()

                    # Update tracker
                    tracker.last_assigned_technician = technician
                    tracker.save()

                    total_assigned += 1
                    self.stdout.write(f"✔️ Booking ID {booking.id} assigned to Technician ID {technician.id}")
                    assigned = True
                    break

            if not assigned:
                self.stdout.write(self.style.WARNING(f"All eligible technicians already have 4 tasks. Booking ID {booking.id} remains unassigned."))

        self.stdout.write(self.style.SUCCESS(f"✅ {total_assigned} bookings assigned based on pincodes, limits, and technician load."))
