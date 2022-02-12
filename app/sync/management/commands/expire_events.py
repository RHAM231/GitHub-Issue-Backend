from repositories.models import Repository
from django.utils import timezone
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist


# Let's add a command to manage.py to allow a cron job on our server to
# periodically delete our Sandbox-Import repo. We'll have cron run the
# command every 15 minutes to check if the repo was created over an
# hour ago.
class Command(BaseCommand):
    help = 'Expires event objects which are out-of-date'
    def handle(self, *args, **kwargs):
        # Try to get our repo
        try:
            repo = Repository.objects.get(name='Sandbox-Import')
            # Get the length of the time the repo has existed in the
            # database
            time_check = timezone.now() - repo.expire_time
            # Set our expiration time to one hour
            expire = timedelta(hours=1)

            # If an hour has passed, delete the repo, otherwise do
            # nothing
            if time_check >= expire:
                print(
                    'Time Check: ', time_check, 
                    'Expire: ', expire, 
                    ' Repository expired, deleting ...'
                )
                repo.delete()
            else:
                print(
                    'Time Check: ', time_check, 
                    'Expire: ', expire, 
                    ' Repository not expired yet, keeping ...'
                )

        except ObjectDoesNotExist:
            print('No repository to delete')
        
