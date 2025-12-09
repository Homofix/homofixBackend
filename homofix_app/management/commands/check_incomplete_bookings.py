from django.core.management.base import BaseCommand
from homofix_app.background_tasks import check_incomplete_bookings

class Command(BaseCommand):
    help = 'Checks for incomplete bookings older than 24 hours and deducts penalty from technician wallet'

    def handle(self, *args, **kwargs):
        check_incomplete_bookings()
        self.stdout.write(self.style.SUCCESS('Successfully checked incomplete bookings and applied penalties'))