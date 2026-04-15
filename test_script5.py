import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homofix_Proj.settings")
django.setup()

from homofix_app.models import Booking
from decimal import Decimal
from homofix_app.HodViews import render_to_pdf

with open('homofix_app/templates/Invoice/invoice.html', 'r') as f:
    text = f.read()

# Try without height: 100% and without bootstrap
text = text.replace('height:100%', 'height:100px')
text = text.replace('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"', '<!--')

with open('homofix_app/templates/Invoice/invoice_test.html', 'w') as f:
    f.write(text)

try:
    b = Booking.objects.get(id=25305)
    
    total_amt = b.total_amount
    tax_amount = b.tax_amount
    grandtotal = b.final_amount
    cgst_sgst = Decimal(grandtotal) * Decimal('0.09')

    pdf_response = render_to_pdf(
        "Invoice/invoice_test.html",
        {
            "booking": b,
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

