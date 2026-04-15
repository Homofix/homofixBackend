import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homofix_Proj.settings")
django.setup()

from homofix_app.models import Booking
from decimal import Decimal
try:
    booking_id = 25618
    from django.template.loader import render_to_string
    b = Booking.objects.get(id=25305)
    print("GOT BOOKING")
    
    total_amt = b.total_amount
    tax_amount = b.tax_amount
    grandtotal = b.final_amount
    cgst_sgst = Decimal(grandtotal) * Decimal('0.09')

    html_content = render_to_string(
        "Invoice/invoice.html",
        {
            "booking": b,
            "addon": [],
            "total": total_amt,
            "cgst_sgst": cgst_sgst,
            "grandtotal": grandtotal,
        },
    )
    print("RENDERED TEMPLATE SUCCESSFULLY")

except Exception as e:
    import traceback
    traceback.print_exc()

