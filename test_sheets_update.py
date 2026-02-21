import os
import django
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homofix_Proj.settings')
django.setup()

from homofix_app.models import Customer
from homofix_app.google_sheets_utils import update_or_append_row

def test_customer_update():
    print("Testing Google Sheets Customer Update...")
    
    # 1. Create dummy data
    customer_id = 99999
    row_data_initial = [
        customer_id,
        "Test User Initial",
        "1234567890",
        "Initial City",
        "Initial State",
        "Initial Area",
        "Initial Address",
        "110001",
        "2024-01-01"
    ]
    
    print(f"1. Appending initial row for ID {customer_id}...")
    try:
        update_or_append_row("Customers", 1, customer_id, row_data_initial)
        print("   -> Initial row appended/updated.")
    except Exception as e:
        print(f"   -> Failed: {e}")
        return

    time.sleep(2) # Wait a bit

    # 2. Update data
    row_data_updated = [
        customer_id,
        "Test User UPDATED",
        "9876543210", # Changed mobile
        "Updated City", # Changed city
        "Updated State",
        "Updated Area",
        "Updated Address",
        "110002",
        "2024-01-02"
    ]

    print(f"2. Updating row for ID {customer_id}...")
    try:
        update_or_append_row("Customers", 1, customer_id, row_data_updated)
        print("   -> Row update triggered. Check Google Sheet for 'Test User UPDATED'.")
    except Exception as e:
        print(f"   -> Failed: {e}")

if __name__ == "__main__":
    test_customer_update()
