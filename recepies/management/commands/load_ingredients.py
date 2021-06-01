from django.core.management.base import BaseCommand
from recepies.models import Ingredient
import csv
from foodgram.settings import BASE_DIR
import os

CSV_FILE_PATH = os.path.join(BASE_DIR, 'ingredients.csv')


class Command(BaseCommand):
    help = 'Load data from .csv'

    def handle(self, *args, **options):
        with open(CSV_FILE_PATH, encoding='UTF-8') as file:
            reader = csv.reader(file)
            for entry in reader:
                title, unit = entry
                Ingredient.objects.get_or_create(title=title, unit=unit)
