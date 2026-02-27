import logging
from django.core.management.base import BaseCommand
from homofix_app.models import Technician
from homofix_app.sheet_sync import sync_technician
import time

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Re-sync all Experts (Technicians) to Google Sheets to update categories and names.'

    def handle(self, *args, **options):
        technicians = Technician.objects.all()
        count = technicians.count()
        self.stdout.write(self.style.SUCCESS(f'Found {count} technicians to sync.'))

        success_count = 0
        for tech in technicians:
            try:
                sync_technician(tech)
                success_count += 1
                self.stdout.write(f"Synced Technician: {tech.id}")
                time.sleep(2.0) # Avoid hitting Google Sheets API rate limits
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to sync Technician {tech.id}: {e}"))

        self.stdout.write(self.style.SUCCESS(f'Successfully re-synced {success_count} out of {count} technicians.'))
