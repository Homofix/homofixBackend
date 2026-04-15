import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homofix_Proj.settings")
django.setup()

from homofix_app.models import Booking
try:
    booking_id = 25618
    from django.test import RequestFactory
    from homofix_app.HodViews import invoice_download
    
    # Just grab any booking ID that might have caused the error if we don't know it, let's try the first one that has a coupon
    bookings_with_coupons = Booking.objects.filter(coupon__isnull=False).order_by('-id')[:5]
    print(bookings_with_coupons)
    request = RequestFactory().get('/dummy/')
    for b in bookings_with_coupons:
        print(f"Testing template for booking {b.id} with coupon")
        response = invoice_download(request, b.id)
        if hasattr(response, 'content'):
            if b"Error" in response.content:
                print(response.content)

except Exception as e:
    import traceback
    traceback.print_exc()

