import logging
from django.core.management.base import BaseCommand
from homofix_app.sheet_sync import sync_all_old_bookings

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Syncs all bookings from database into the 'All Old Bookings' tab in Google Sheets."

    def add_arguments(self, parser):
        parser.add_argument(
            '--tab-name',
            type=str,
            default='All Old Bookings',
            help="Name of the Google Sheets tab (default: 'All Old Bookings')",
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help="Number of rows per API batch request (default: 100)",
        )
        parser.add_argument(
            '--delay',
            type=float,
            default=0.5,
            help="Delay in seconds between requests to avoid rate limits (default: 0.5)",
        )

    def handle(self, *args, **options):
        tab_name = options['tab_name']
        batch_size = options['batch_size']
        delay = options['delay']

        self.stdout.write(f"Starting sync of all bookings to Google Sheets tab '{tab_name}'...")
        count = sync_all_old_bookings(tab_name=tab_name, batch_size=batch_size, delay=delay)
        self.stdout.write(self.style.SUCCESS(f"Successfully processed {count} bookings for tab '{tab_name}'."))
