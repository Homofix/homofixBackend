import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homofix_Proj.settings")
django.setup()

from homofix_app.models import Booking
from decimal import Decimal
from homofix_app.HodViews import render_to_pdf

with open('homofix_app/templates/Invoice/invoice.html', 'r') as f:
    text = f.read()

# Make changes to text to test
text = text.replace('<img src="/home/ubuntu/homofixBackend/static/logodark.png" class="logo">', 
                    '{% get_logo_base64 as logo_base64 %}\n        <img src="{{ logo_base64 }}" class="logo">')

# Fix addon empty row
text = text.replace('<td></td>', '<td>&nbsp;</td>')

with open('homofix_app/templates/Invoice/invoice_test.html', 'w') as f:
    f.write(text)

try:
    b = Booking.objects.get(id=25305)
    pdf_response = render_to_pdf(
        "Invoice/invoice_test.html",
        {
            "booking": b,
            "addon": [],
            "total": b.total_amount,
            "cgst_sgst": Decimal(b.final_amount) * Decimal('0.09'),
            "grandtotal": b.final_amount,
        },
    )
    with open('test_out.pdf', 'wb') as f:
        f.write(pdf_response.content)
    print("HEIGHT FIX ONLY WORKED, WROTE TO test_out.pdf")
except Exception:
    import traceback
    traceback.print_exc()

