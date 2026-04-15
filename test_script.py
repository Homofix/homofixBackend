import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homofix_Proj.settings")
django.setup()

from homofix_app.models import Booking
try:
    for booking in Booking.objects.order_by('-id')[:10]:
        print(f"Testing booking {booking.id}")
        t = booking.total_amount
        b = booking.tax_amount
        c = booking.final_amount
except Exception as e:
    import traceback
    traceback.print_exc()

