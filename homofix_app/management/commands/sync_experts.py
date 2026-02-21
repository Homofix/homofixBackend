from django.core.management.base import BaseCommand
from homofix_app.models import Technician
from homofix_app.sheet_sync import sync_technician
import time

class Command(BaseCommand):
    help = 'Syncs all existing experts to the Experts Google Sheet'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting expert sync to Google Sheets...")

        technicians = Technician.objects.all()
        total = technicians.count()
        self.stdout.write(f"Found {total} Technicians. Syncing...")
        
        synced_count = 0
        error_count = 0

        for tech in technicians:
             try:
                sync_technician(tech)
                synced_count += 1
                self.stdout.write(f"Successfully synced Expert: {tech.expert_id} ({synced_count}/{total})")
                time.sleep(2.0) # Avoid hitting Google Sheets API rate limits
             except Exception as e:
                error_count += 1
                self.stdout.write(self.style.ERROR(f"Error syncing Expert {tech.expert_id or tech.id}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Expert sync completed! Synced: {synced_count}, Errors: {error_count}"))
