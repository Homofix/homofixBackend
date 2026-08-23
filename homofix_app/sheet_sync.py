import time
import logging
import gspread
from .models import Customer, Booking, Technician, RechargeHistory, Task, SLOT_CHOICES_DICT
from .google_sheets_utils import (
    append_to_sheet,
    update_or_append_row,
    append_rows_to_sheet,
    get_gspread_client,
    SPREADSHEET_ID,
)

logger = logging.getLogger(__name__)


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
    # Try to find all tasks for this booking, ordered by creation time
    tasks = Task.objects.filter(booking=booking).order_by('created_at')
    
    first_expert_id = "N/A"
    first_expert_name = "N/A"
    reassigned_expert_id = ""
    reassigned_expert_name = ""

    if tasks.exists():
        first_task = tasks.first()
        first_expert_id = first_task.technician.expert_id
        first_expert_name = first_task.technician.admin.username if first_task.technician.admin else "Unknown"

        if tasks.count() > 1:
            last_task = tasks.last()
            reassigned_expert_id = last_task.technician.expert_id
            reassigned_expert_name = last_task.technician.admin.username if last_task.technician.admin else "Unknown"
    
    # If a specific technician was passed (e.g., from signals on create), we might use them
    # but the tasks query above is more reliable for checking history (reassignments).
    
    first_expert_display = f"{first_expert_id} ({first_expert_name})" if first_expert_id and first_expert_id != "N/A" else ""
    reassigned_expert_display = f"{reassigned_expert_id} ({reassigned_expert_name})" if reassigned_expert_id else ""
    
    try:
        slot_int = int(booking.slot) if booking.slot is not None else None
        slot_display = SLOT_CHOICES_DICT.get(slot_int, booking.slot)
    except:
        slot_display = booking.slot

    booking_amt = booking.subtotal
    booking_total_amount = booking.total_amount
    addons_amt = booking.total_addons
    discount_amt = booking.coupon_discount_amount if booking.coupon else 0
    total_amt = booking.final_amount
    
    invoice_no = ""
    if status == "Completed":
        try:
            from .models import Invoice
            invoice = Invoice.objects.filter(booking_id=booking).first()
            if invoice:
                invoice_no = invoice.invoice_no
        except Exception:
            pass
        
    tax_value = getattr(booking, 'tax_amount', 0)
    
    completed_date = booking.booking_date.strftime('%Y-%m-%d') if status == "Completed" and booking.booking_date else ""
    payment_mode = "Online" if booking.online else "Cash"
    
    cust_name = booking.booking_customer or (booking.customer.admin.first_name if booking.customer and hasattr(booking.customer, 'admin') else "")
    cust_mobile = booking.mobile or (booking.customer.mobile if booking.customer else "")
    cust_city = booking.city or (booking.customer.city if booking.customer else "")
    cust_state = booking.state or (booking.customer.state if booking.customer else "")
    cust_zipcode = booking.zipcode or (booking.customer.zipcode if booking.customer else "")
    
    b_addr = booking.booking_address or (booking.customer.address if booking.customer else "")
    b_area = booking.area or (booking.customer.area if booking.customer else "")
    
    b_addr = "" if str(b_addr).strip().lower() == "none" else str(b_addr).strip()
    b_area = "" if str(b_area).strip().lower() == "none" else str(b_area).strip()
    
    if b_addr and b_area:
        cust_address = f"{b_addr}, {b_area}"
    else:
        cust_address = b_addr or b_area or ""
        
    cust_name = "" if str(cust_name).lower() == "none" else cust_name
    cust_city = "" if str(cust_city).lower() == "none" else cust_city
    cust_state = "" if str(cust_state).lower() == "none" else cust_state
    cust_zipcode = "" if str(cust_zipcode).lower() == "none" else cust_zipcode
    cust_mobile = "" if str(cust_mobile).lower() == "none" else cust_mobile

    row_data = [
        booking.id, 
        booking.order_id,
        first_expert_display, 
        get_subcategory_str(booking),
        get_products_str(booking),
        cust_name, 
        cust_mobile,
        cust_city,
        cust_state,
        cust_address,
        cust_zipcode,
        booking_amt,
        booking_total_amount,
        addons_amt,
        discount_amt,
        tax_value,
        total_amt,
        booking.booking_date.strftime('%Y-%m-%d') if booking.booking_date else "",
        completed_date,
        slot_display, 
        payment_mode, 
        get_order_by(booking),
        status,
        booking.cancel_reason if status == "Cancelled" else "",
        reassigned_expert_display,
        invoice_no
        
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

    admin = getattr(instance, 'admin', None)
    username = admin.username if admin else ""
    first_name = admin.first_name if admin and admin.first_name else ""
    last_name = admin.last_name if admin and admin.last_name else ""
    
    # Extract Category from Subcategories
    try:
        categories = set([sc.Category_id.category_name for sc in instance.subcategories.all() if sc.Category_id])
        category_str = ", ".join(categories)
    except:
        category_str = ""

    expert_display = f"{instance.expert_id} ({username})" if username and instance.expert_id else str(instance.expert_id or "")
        
    row_data = [
        instance.id,
        expert_display,
        category_str, 
        subcats,
        instance.state,
        instance.city,
        instance.serving_area,
        pincodes,
        instance.status,
        "Active", 
        str(wallet_amt),
        instance.mobile
    ]
    update_or_append_row("Experts", 1, instance.id, row_data)

def sync_recharge(instance):
    tech = instance.technician_id
    admin = getattr(tech, 'admin', None)
    username = admin.username if admin else ""
    first_name = admin.first_name if admin and admin.first_name else ""
    last_name = admin.last_name if admin and admin.last_name else ""
    
    name = f"{first_name} {last_name}".strip()
    if not name:
        name = username

    expert_display = f"{tech.expert_id} ({username})" if username and tech.expert_id else str(tech.expert_id or "")

    row_data = [
        expert_display,
        name,
        instance.payment_id,
        instance.amount,
        instance.date
    ]
    append_to_sheet("Recharge", row_data)


def sync_old_booking(booking, tab_name="All Old Bookings"):
    """
    Syncs a single booking to the specified tab (default: 'All Old Bookings').
    Data format is identical to 'All Bookings'.
    """
    row_data = get_booking_row_data(booking, booking.status)
    update_or_append_row(tab_name, 1, booking.id, row_data)


def sync_all_old_bookings(tab_name="All Old Bookings", batch_size=500, delay=1.0):
    """
    Syncs all bookings from the database into the specified Google Sheet tab (default: 'All Old Bookings').
    Data entry structure is identical to 'All Bookings'.
    Uses bulk matrix fetching and chunked updates with 429 quota auto-retry to prevent API limits.
    """
    bookings = Booking.objects.all().order_by('id')
    total_count = bookings.count()
    logger.info(f"Starting bulk sync of {total_count} bookings to '{tab_name}'...")

    client = get_gspread_client()
    if not client:
        logger.error("Failed to authenticate with Google Sheets client.")
        return 0

    def retry_api_call(func, *args, max_retries=5, initial_wait=10, **kwargs):
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except gspread.exceptions.APIError as e:
                if '429' in str(e) or 'Quota exceeded' in str(e):
                    wait_time = initial_wait * (2 ** attempt)
                    logger.warning(f"Google API Quota exceeded (429). Waiting {wait_time} seconds before retry (attempt {attempt + 1}/{max_retries})...")
                    time.sleep(wait_time)
                else:
                    raise e
        raise Exception("Max retries exceeded for Google Sheets API call.")

    try:
        sheet = retry_api_call(client.open_by_key, SPREADSHEET_ID)
        try:
            worksheet = sheet.worksheet(tab_name)
        except gspread.exceptions.WorksheetNotFound:
            try:
                sheet = retry_api_call(client.open_by_key, '1UwskHVXLjzKzlXslKIG3eTPTG6sO1zaFjWn1_pSpLbs')
                worksheet = sheet.worksheet(tab_name)
            except Exception as e:
                logger.error(f"Worksheet '{tab_name}' not found: {e}")
                return 0

        # FETCH ALL EXISTING ROWS IN A SINGLE API CALL
        all_rows = retry_api_call(worksheet.get_all_values)
        
        # Index existing booking IDs in sheet
        existing_map = {}
        if len(all_rows) > 1:
            for idx, row in enumerate(all_rows[1:], start=1):
                if row:
                    b_id_str = str(row[0]).strip()
                    if b_id_str:
                        existing_map[b_id_str] = idx

        header = all_rows[0] if all_rows else [
            "S.No", "Order ID", "Assigned Expert", "Sub Category", "Product Name",
            "Customer Name", "Customer Mobile", "City", "State", "Address",
            "Pincode", "Booking Amount", "Total Amount", "Addons Amount",
            "Discount Amount", "Tax Value", "Final Amount", "Booking Date",
            "Completed Date", "Slot", "Payment Mode", "Order By", "Status",
            "Cancel Reason", "Reassigned Expert", "Invoice No"
        ]

        new_rows_matrix = [header]
        synced_count = 0

        for booking in bookings:
            row_data = get_booking_row_data(booking, booking.status)
            formatted_row = [str(item) if item is not None else "" for item in row_data]
            booking_id_str = str(booking.id).strip()

            if booking_id_str in existing_map:
                row_idx = existing_map[booking_id_str]
                if row_idx < len(all_rows):
                    old_row = all_rows[row_idx]
                    # Preserve 'Assigned Expert' and handle 'Reassigned Expert'
                    if len(old_row) > 2 and old_row[2].strip():
                        old_expert = old_row[2].strip()
                        new_expert = str(row_data[2]).strip() if len(row_data) > 2 else ""
                        
                        if old_expert and new_expert and old_expert != new_expert:
                            formatted_row[2] = old_expert
                            if len(formatted_row) > 24:
                                formatted_row[24] = new_expert
                        elif old_expert == new_expert:
                            if len(old_row) > 24 and old_row[24].strip():
                                if len(formatted_row) > 24:
                                    formatted_row[24] = old_row[24].strip()

            new_rows_matrix.append(formatted_row)
            synced_count += 1

        total_rows_needed = len(new_rows_matrix)
        total_cols_needed = max(len(r) for r in new_rows_matrix) if new_rows_matrix else 26

        # Resize worksheet if needed
        if worksheet.row_count < total_rows_needed or worksheet.col_count < total_cols_needed:
            logger.info(f"Resizing worksheet '{tab_name}' to {total_rows_needed} rows x {total_cols_needed} cols...")
            retry_api_call(worksheet.resize, rows=total_rows_needed, cols=total_cols_needed)

        # WRITE MATRIX IN CHUNKS
        start_row = 1
        for i in range(0, len(new_rows_matrix), batch_size):
            chunk = new_rows_matrix[i:i + batch_size]
            end_row = start_row + len(chunk) - 1
            range_name = f"A{start_row}:Z{end_row}"
            logger.info(f"Updating rows {start_row} to {end_row} in '{tab_name}'...")
            retry_api_call(worksheet.update, values=chunk, range_name=range_name)
            start_row = end_row + 1
            if delay > 0 and (i + batch_size) < len(new_rows_matrix):
                time.sleep(delay)

        # Trim trailing blank rows
        if worksheet.row_count > total_rows_needed + 10:
            retry_api_call(worksheet.resize, rows=total_rows_needed + 10, cols=total_cols_needed)

        logger.info(f"Successfully synced {synced_count} bookings to '{tab_name}' in bulk.")
        return synced_count

    except Exception as e:
        logger.error(f"Error syncing all old bookings to '{tab_name}': {e}")
        return 0


