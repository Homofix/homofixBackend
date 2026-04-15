import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homofix_Proj.settings")
django.setup()

from homofix_app.models import Booking
from decimal import Decimal
from homofix_app.HodViews import render_to_pdf

try:
    b = Booking.objects.get(id=25305)
    print("GOT BOOKING")
    
    total_amt = b.total_amount
    tax_amount = b.tax_amount
    grandtotal = b.final_amount
    cgst_sgst = Decimal(grandtotal) * Decimal('0.09')

    # Note passing correct arguments corresponding to what's done in HodViews
    pdf_response = render_to_pdf(
        "Invoice/invoice.html",
        {
            "booking": b, # In my code I passed invoice, not booking? Wait!!!
            "addon": [],
            "total": total_amt,
            "cgst_sgst": cgst_sgst,
            "grandtotal": grandtotal,
        },
    )
    print("RENDERED PDF SUCCESSFULLY")
except Exception as e:
    import traceback
    traceback.print_exc()

