from homofix_app .models import Technician,AutoAssignSetting,UniversalCredential,Slot,TechnicianAssignmentTracker,Task,Wallet
from django.db.models import Count
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, time
from decimal import Decimal
from utils.firebase import send_push_notification
from utils.background import run_in_background

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
        print("booking.booking_date:", booking.booking_date.date())
        print("booking.slot:", booking.slot)
        print("booking.zipcode:", booking.zipcode)
        print("subcategory_ids:", subcategory_ids)

        # --------------------------
        # Technician Filtering Logic
        # --------------------------

        # Fetch technicians in pincode first
        techs_in_pincode = Technician.objects.filter(
            working_pincode_areas__code=int(booking.zipcode),showonline__online=1
        ).prefetch_related("subcategories").distinct()

        # Now filter in Python for subcategory match
        filtered_techs = []
        for tech in techs_in_pincode:
            tech_subcats = list(tech.subcategories.values_list("id", flat=True))
            if any(subcat in tech_subcats for subcat in subcategory_ids):
                filtered_techs.append(tech)

        # Sort technicians by rating (descending) for prioritized round-robin
        def get_rating(t):
            try:
                # Handle CharField: remove non-numeric chars if needed, convert to float
                return float(t.rating) if t.rating else 0.0
            except ValueError:
                return 0.0
        
        filtered_techs.sort(key=get_rating, reverse=True)

        if not filtered_techs:
            print("❌ No matching technicians found for this pincode & subcategory.")
            return None

        print(f"✅ Technicians found: {[t.id for t in filtered_techs]}")

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
        # Technician Round-robin Logic
        # -----------------------------

        tracker = TechnicianAssignmentTracker.objects.first()
        technician_list = list(filtered_techs)
        tech_ids = [t.id for t in technician_list]

        # Bulk fetch Wallets
        # Assuming technician_id is the field name in Wallet model
        wallets = Wallet.objects.filter(technician_id__in=tech_ids)
        # Create a map of technician_id -> total_share
        wallet_map = {w.technician_id: w.total_share for w in wallets}

        # Bulk fetch Task Counts for Today
        task_counts_qs = Task.objects.filter(
            technician__id__in=tech_ids,
            booking__booking_date__date=booking.booking_date.date()
        ).values('technician').annotate(count=Count('id'))
        
        task_count_map = {item['technician']: item['count'] for item in task_counts_qs}

        # Find where to start in round-robin
        start_index = 0
        if tracker and tracker.last_assigned_technician:
            last_id = tracker.last_assigned_technician.id
            ids = [t.id for t in technician_list]
            if last_id in ids:
                start_index = (ids.index(last_id) + 1) % len(ids)

        assigned = False
        max_tasks_per_technician = 4

        for i in range(len(technician_list)):
            tech = technician_list[(start_index + i) % len(technician_list)]

            # Check wallet from map (avoid N+1 query)
            total_share = wallet_map.get(tech.id)
            
            # If no wallet found or balance < 1000, skip
            if total_share is None or total_share < Decimal("1000.00"):
                print(f"⚠ Technician {tech.id} skipped (wallet balance < 1000).")
                continue

            # Check active tasks from map (avoid N+1 query)
            active_tasks = task_count_map.get(tech.id, 0)

            if active_tasks < max_tasks_per_technician:
                # ✅ Assign technician
                booking.status = 'Assign'
                booking.save()

                task = Task.objects.create(
                    booking=booking,
                    technician=tech,
                    description=f"Auto assigned task for booking {booking.id}",
                    supported_by=None,
                )

                if tech.fcm_token:
                    # Async notification
                    run_in_background(
                        send_push_notification,
                        token=tech.fcm_token,
                        title="New Task Assigned",
                        body=f"Booking #{booking.id} ka task aapko assign hua hai.",
                        data={"booking_id": str(booking.id), "task_id": str(task.id)}
                    )

                # Update tracker
                if not tracker:
                    tracker = TechnicianAssignmentTracker.objects.create(
                        last_assigned_technician=tech
                    )
                else:
                    tracker.last_assigned_technician = tech
                    tracker.save()

                print(f"✅ Task created for Technician {tech.id}. Technician total tasks today: {active_tasks + 1}")
                assigned = True
                break
            else:
                print(f"⚠ Technician {tech.id} already has {active_tasks} tasks today. Skipping.")

        if not assigned:
            print("❌ All technicians reached their max per-day task limit. No assignment done.")

    except Exception as e:
        print("Auto assignment error:", e)
        return None