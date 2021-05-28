from repositories.models import Repository
from django.utils import timezone
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):
    help = 'Expires event objects which are out-of-date'
    def handle(self, *args, **kwargs):
        try:
            repo = Repository.objects.get(name='Sandbox-Import')
            time_check = timezone.now() - repo.expire_time
            expire = timedelta(hours=1)

            if time_check >= expire:
                print('Repository expired, deleting ...')
                repo.delete()
            else:
                print('Repository not expired yet, keeping ...')

        except ObjectDoesNotExist:
            print('No repository to delete')
        