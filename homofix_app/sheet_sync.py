from .models import Customer, Booking, Technician, RechargeHistory, Task, SLOT_CHOICES_DICT
from .google_sheets_utils import append_to_sheet, update_or_append_row

# --- Helpers ---

def get_products_str(booking):
    products = booking.booking_product.all()
    return ", ".join([bp.product.name for bp in products]) if products else ""

def get_subcategory_str(booking):
    products = booking.booking_product.all()
    # Assuming subcategory is linked to Product.model: product.subcategory.name
    subcats = set([bp.product.subcategory.name for bp in products if bp.product.subcategory])
    return ", ".join(subcats)

def get_assigned_expert_info(booking):
    # Try to find the expert from the latest 'Assign' task
    task = Task.objects.filter(booking=booking).order_by('-created_at').first()
    if task:
        return task.technician.expert_id, task.technician.admin.username 
    return "N/A", "N/A"

def get_order_by(booking):
     if booking.supported_by:
         return booking.supported_by.admin.username
     elif booking.admin_by:
         return booking.admin_by.admin.username
     else:
         return "Customer"

# --- Sync Functions ---

def sync_customer(instance):
    # {Customers : [S.No , Name , Mobile No , City , State , Area , Address ,Pin Code, Date ]}
    row_data = [
        instance.id,
        instance.admin.first_name + " " + instance.admin.last_name, 
        instance.mobile,
        instance.city,
        instance.state,
        instance.area, # Area
        f"{instance.address}, {instance.area}", # Full Address
        instance.zipcode,
        instance.date
    ]
    update_or_append_row("Customers", 1, instance.id, row_data)

def get_booking_row_data(booking, status, technician=None):
    if not technician:
        expert_id, expert_name = get_assigned_expert_info(booking)
    else:
        expert_id = technician.expert_id
        expert_name = technician.admin.username if technician and technician.admin else "Unknown"
        
    expert_display = f"{expert_id} ({expert_name})" if expert_id and expert_id != "N/A" else ""
    
    try:
        slot_int = int(booking.slot) if booking.slot is not None else None
        slot_display = SLOT_CHOICES_DICT.get(slot_int, booking.slot)
    except:
        slot_display = booking.slot

    booking_amt = booking.total_amount
    addons_amt = booking.total_addons
    discount_amt = booking.coupon_discount_amount if booking.coupon else 0
    total_amt = booking.final_amount
    
    completed_date = booking.booking_date.strftime('%b. %d, %Y') if status == "Completed" and booking.booking_date else ""
    payment_mode = "Online" if booking.online else "Cash"
    
    row_data = [
        booking.id, 
        booking.order_id,
        expert_display, 
        get_subcategory_str(booking),
        get_products_str(booking),
        booking.customer.admin.first_name if booking.customer and booking.customer.admin else "", 
        booking.customer.mobile if booking.customer else "",
        booking.customer.city if booking.customer else "",
        booking.customer.state if booking.customer else "",
        f"{booking.customer.address}, {booking.customer.area}" if booking.customer else "",
        booking.customer.zipcode if booking.customer else "",
        booking_amt,
        addons_amt,
        discount_amt,
        total_amt,
        booking.booking_date.strftime('%b. %d, %Y') if booking.booking_date else "",
        completed_date,
        slot_display, 
        payment_mode, 
        get_order_by(booking),
        status,
        booking.cancel_reason if status == "Cancelled" else ""
    ]
    return row_data

def sync_assigned_booking(booking, technician=None):
    row_data = get_booking_row_data(booking, "Assigned", technician)
    update_or_append_row("All Bookings", 1, booking.id, row_data)

def sync_completed_booking(booking):
    row_data = get_booking_row_data(booking, "Completed")
    update_or_append_row("All Bookings", 1, booking.id, row_data)

def sync_cancelled_booking(booking):
    row_data = get_booking_row_data(booking, "Cancelled")
    update_or_append_row("All Bookings", 1, booking.id, row_data)

def sync_new_booking(booking):
    row_data = get_booking_row_data(booking, "New")
    update_or_append_row("All Bookings", 1, booking.id, row_data)

def sync_technician(instance):
    try:
        subcats = ", ".join([sc.name for sc in instance.subcategories.all()])
    except:
        subcats = ""
        
    try:
        pincodes = ", ".join([str(pc.code) for pc in instance.working_pincode_areas.all()])
    except:
        pincodes = ""

    try:
        wallet_amt = instance.wallet_set.first().total_share
    except:
        wallet_amt = 0

    try:
        name = instance.admin.first_name + " " + instance.admin.last_name
    except:
        name = instance.admin.username if getattr(instance, 'admin', None) else ""
        
    row_data = [
        instance.id,
        instance.expert_id,
        name, 
        subcats,
        instance.state,
        instance.city,
        instance.serving_area,
        pincodes,
        instance.status,
        "Active", 
        str(wallet_amt)
    ]
    update_or_append_row("Experts", 1, instance.id, row_data)

def sync_recharge(instance):
    row_data = [
        instance.technician_id.expert_id,
        instance.technician_id.admin.first_name,
        instance.payment_id,
        instance.amount,
        instance.date
    ]
    append_to_sheet("Recharge", row_data)
