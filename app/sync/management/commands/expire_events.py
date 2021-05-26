from repositories.models import Repository
from django.utils import timesince, timezone
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Expires event objects which are out-of-date'
    def handle(self, *args, **kwargs):
        print('test')
        Repository.objects.filter(name='Sandbox-Import').delete()