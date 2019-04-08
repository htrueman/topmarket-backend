from django.core.management.base import BaseCommand
from catalog.models import Category


class Command(BaseCommand):
    help = 'Load categories'

    def handle(self, *args, **options):
        Category.load_categories()

        self.stdout.write(self.style.SUCCESS('Categories loaded.'))
