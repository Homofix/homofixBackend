from homofix_app .models import Technician,AutoAssignSetting,UniversalCredential,Slot,TechnicianAssignmentTracker,Task,Wallet, feedback
from django.db.models import Count, Avg
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, time
from decimal import Decimal
from utils.firebase import send_push_notification

# def assign_employee_to_booking(booking):
#     print("🟢 assign_employee_to_booking function CALLED!")

#     try:
#         # Check if auto-assign feature is ON
#         auto_assign_enabled = AutoAssignSetting.objects.first()
#         if not auto_assign_enabled or not auto_assign_enabled.is_enabled:
#             print("❌ Auto-assign is disabled.")
#             return None

#         # Universal slot limit
#         universal_cred = UniversalCredential.objects.first()
#         universal_limit = universal_cred.universal_slot if universal_cred and universal_cred.universal_slot else 0

#         # Booking's subcategories
#         subcategory_ids = list(
#             booking.products.values_list('subcategory__id', flat=True).distinct()
#         )
       

#         # --------------------------
#         # Technician Filtering Logic
#         # --------------------------

#         # Fetch technicians in pincode first, annotated with average rating
#         techs_in_pincode = Technician.objects.filter(
#             working_pincode_areas__code=int(booking.zipcode),showonline__online=1
#         ).annotate(avg_rating=Avg('feedback__rating')).prefetch_related("subcategories").distinct()

#         # Now filter in Python for subcategory match
#         filtered_techs = []
#         for tech in techs_in_pincode:
#             tech_subcats = list(tech.subcategories.values_list("id", flat=True))
#             if any(subcat in tech_subcats for subcat in subcategory_ids):
#                 filtered_techs.append(tech)

#         if not filtered_techs:
#             print("❌ No matching technicians found for this pincode & subcategory.")
#             return None

#         # Sort by rating (descending), treat None as 0
#         filtered_techs.sort(key=lambda x: x.avg_rating or 0, reverse=True)

#         print(f"✅ Technicians found (sorted by rating): {[f'{t.id} (Rating: {t.avg_rating})' for t in filtered_techs]}")

#         # ----------------------
#         # Slot Lookup Logic
#         # ----------------------

#         # Slot filter logic:
#         # Check slots that:
#         # - have the same date
#         # - same slot no.
#         # - any matching pincode
#         # - any matching subcategory
#         slot_qs = Slot.objects.filter(
#             date=booking.booking_date.date(),
#             slot=booking.slot,
#             pincode__code=int(booking.zipcode),
#             subcategories__id__in=subcategory_ids
#         ).distinct()

#         if slot_qs.exists():
#             # Minimum limit among matching slots
#             slot_limits = [s.limit for s in slot_qs if s.limit is not None]
#             if slot_limits:
#                 slot_limit = min(slot_limits)
#             else:
#                 slot_limit = universal_limit
#             print(f"✅ Slots found. Smallest limit = {slot_limit}")
#         else:
#             slot_limit = universal_limit
#             print("⚠ No specific slot found, falling back to universal slot limit.")

#         if slot_limit == 0:
#             print("❌ Slot limit or universal limit is zero. Cannot assign task.")
#             return None

#         # ----------------------------
#         # Check Existing Tasks in Slot
#         # ----------------------------
#         existing_tasks_count = Task.objects.filter(
#             booking__booking_date__date=booking.booking_date.date(),
#             booking__slot=booking.slot,
#             booking__zipcode=booking.zipcode,
#             booking__products__subcategory__id__in=subcategory_ids
#         ).distinct().count()

#         print(f"ℹ Existing tasks in this slot: {existing_tasks_count} of allowed {slot_limit}")

#         if existing_tasks_count >= slot_limit:
#             print("❌ Slot limit reached. No further assignment.")
#             return None

#         # -----------------------------
#         # Technician Priority Logic (Based on Rating)
#         # -----------------------------

#         technician_list = filtered_techs # Already sorted by rating

#         assigned = False
#         max_tasks_per_technician = 4

#         for tech in technician_list:
#             wallet = Wallet.objects.filter(technician_id=tech).first()
#             if not wallet or wallet.total_share < Decimal("1000.00"):
#                 print(f"⚠ Technician {tech.id} skipped (wallet balance < 1000).")
#                 continue  # Skip this technician

            
#             active_tasks = Task.objects.filter(
#                 technician=tech,
#                 booking__booking_date__date=booking.booking_date.date()
#             ).count()

#             if active_tasks < max_tasks_per_technician:
#                 # ✅ Assign technician
#                 booking.status = 'Assign'
#                 booking.save()

#                 task = Task.objects.create(
#                     booking=booking,
#                     technician=tech,
#                     description=f"Auto assigned task for booking {booking.id}",
#                     supported_by=None,
#                 )

#                 if tech.fcm_token:  # maan ke chalte hain Technician model me fcm_token field hai
#                     send_push_notification(
#                         token=tech.fcm_token,
#                         title="New Task Assigned",
#                         body=f"Booking #{booking.id} ka task aapko assign hua hai.",
#                         data={"booking_id": str(booking.id), "task_id": str(task.id)}
#                     )

#                 # ✅ Update Slot Limits for ALL matched slots
#                 # if slot_qs.exists():
#                 #     for slot_obj in slot_qs:
#                 #         if slot_obj.limit is not None and slot_obj.limit > 0:
#                 #             slot_obj.limit -= 1
#                 #             slot_obj.save()
#                 #             print(f"🟢 Slot ID {slot_obj.id} limit decreased. New limit: {slot_obj.limit}")

#                 print(f"✅ Task created for Technician {tech.id}. Technician total tasks today: {active_tasks + 1}")
#                 assigned = True
#                 break
#             else:
#                 print(f"⚠ Technician {tech.id} already has {active_tasks} tasks today. Skipping.")

#         if not assigned:
#             print("❌ All technicians reached their max per-day task limit. No assignment done.")

#     except Exception as e:
#         print("Auto assignment error:", e)
#         return None


def assign_employee_to_booking(booking):
    print("🟢 assign_employee_to_booking function CALLED!")

    try:
        # Check if auto-assign feature is ON
        auto_assign_enabled = AutoAssignSetting.objects.first()
        if not auto_assign_enabled or not auto_assign_enabled.is_enabled:
            print("❌ Auto-assign is disabled.")
            return None

        # Universal slot limit
        universal_cred = UniversalCredential.objects.first()
        universal_limit = universal_cred.universal_slot if universal_cred and universal_cred.universal_slot else 0

        # Booking's subcategories
        subcategory_ids = list(
            booking.products.values_list('subcategory__id', flat=True).distinct()
        )
       

        # --------------------------
        # Technician Filtering Logic
        # --------------------------

        # Fetch technicians in pincode first, annotated with average rating
        techs_in_pincode = Technician.objects.filter(
            working_pincode_areas__code=int(booking.zipcode),showonline__online=1
        ).annotate(avg_rating=Avg('feedback__rating')).prefetch_related("subcategories").distinct()

        # Now filter in Python for subcategory match
        filtered_techs = []
        for tech in techs_in_pincode:
            tech_subcats = list(tech.subcategories.values_list("id", flat=True))
            if any(subcat in tech_subcats for subcat in subcategory_ids):
                filtered_techs.append(tech)

        if not filtered_techs:
            print("❌ No matching technicians found for this pincode & subcategory.")
            return None

        # Sort by rating (descending), treat None as 0
        filtered_techs.sort(key=lambda x: x.avg_rating or 0, reverse=True)

        print(f"✅ Technicians found (sorted by rating): {[f'{t.id} (Rating: {t.avg_rating})' for t in filtered_techs]}")

        # ----------------------
        # Slot Lookup Logic
        # ----------------------

        # Slot filter logic:
        # Check slots that:
        # - have the same date
        # - same slot no.
        # - any matching pincode
        # - any matching subcategory
        slot_qs = Slot.objects.filter(
            date=booking.booking_date.date(),
            slot=booking.slot,
            pincode__code=int(booking.zipcode),
            subcategories__id__in=subcategory_ids
        ).distinct()

        if slot_qs.exists():
            # Minimum limit among matching slots
            slot_limits = [s.limit for s in slot_qs if s.limit is not None]
            if slot_limits:
                slot_limit = min(slot_limits)
            else:
                slot_limit = universal_limit
            print(f"✅ Slots found. Smallest limit = {slot_limit}")
        else:
            slot_limit = universal_limit
            print("⚠ No specific slot found, falling back to universal slot limit.")

        if slot_limit == 0:
            print("❌ Slot limit or universal limit is zero. Cannot assign task.")
            return None

        # ----------------------------
        # Check Existing Tasks in Slot
        # ----------------------------
        existing_tasks_count = Task.objects.filter(
            booking__booking_date__date=booking.booking_date.date(),
            booking__slot=booking.slot,
            booking__zipcode=booking.zipcode,
            booking__products__subcategory__id__in=subcategory_ids
        ).distinct().count()

        print(f"ℹ Existing tasks in this slot: {existing_tasks_count} of allowed {slot_limit}")

        if existing_tasks_count >= slot_limit:
            print("❌ Slot limit reached. No further assignment.")
            return None

        # -----------------------------
        # Technician Priority Logic (Round-Robin by Rank)
        # -----------------------------

        # For round-robin matching, we want to assign to the technician with the LEAST
        # number of active tasks for the day, and tie-break by highest rating.
        # We also need to skip technicians who already have a task in the exact same slot.

        technician_load = []

        for tech in filtered_techs: # filtered_techs is already sorted by rating
            wallet = Wallet.objects.filter(technician_id=tech).first()
            if not wallet or wallet.total_share < Decimal("1000.00"):
                print(f"⚠ Technician {tech.id} skipped (wallet balance < 1000).")
                continue  # Skip this technician
            
            # Check if this tech already has a task in the EXCACT same slot
            has_slot_clash = Task.objects.filter(
                technician=tech,
                booking__booking_date__date=booking.booking_date.date(),
                booking__slot=booking.slot
            ).exists()

            if has_slot_clash:
                print(f"⚠ Technician {tech.id} skipped (already booked for slot {booking.slot}).")
                continue
            
            # Count how many total tasks they have today for distribution balancing
            active_tasks = Task.objects.filter(
                technician=tech,
                booking__booking_date__date=booking.booking_date.date()
            ).count()

            # Append as tuple: (tech, active_tasks, avg_rating)
            technician_load.append((tech, active_tasks, tech.avg_rating or 0))

        if not technician_load:
            print("❌ No eligible technicians available for this slot (all booked or skipped).")
            return None

        # Sort by active_tasks (ascending), then rating (descending)
        technician_load.sort(key=lambda x: (x[1], -x[2]))

        # The first technician in the sorted list is the winner
        assigned_tech = technician_load[0][0]
        assigned_tasks_count = technician_load[0][1]

        print(f"✅ Assigning to Technician {assigned_tech.id} (Today's tasks: {assigned_tasks_count}, Rating: {assigned_tech.avg_rating})")

        # ✅ Assign technician
        booking.status = 'Assign'
        booking.save()

        task = Task.objects.create(
            booking=booking,
            technician=assigned_tech,
            description=f"Auto assigned task for booking {booking.id}",
            supported_by=None,
        )

        if assigned_tech.fcm_token:
            send_push_notification(
                token=assigned_tech.fcm_token,
                title="New Task Assigned",
                body=f"Booking #{booking.id} ka task aapko assign hua hai.",
                data={"booking_id": str(booking.id), "task_id": str(task.id)}
            )

        print(f"✅ Task created for Technician {assigned_tech.id}. Technician total tasks today: {assigned_tasks_count + 1}")

    except Exception as e:
        print("Auto assignment error:", e)
        return None