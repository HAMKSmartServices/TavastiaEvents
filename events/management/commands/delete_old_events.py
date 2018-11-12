from django.core.management.base import BaseCommand, CommandError
from events.models import Event

class Command(BaseCommand):
    help = 'Delete old events'

    """def add_arguments(self, parser):
        parser.add_argument('event_id', nargs='+', type=str)

    def handle(self, *args, **options):
        for poll_id in options['poll_id']:
            try:
                poll = Poll.objects.get(pk=poll_id)
            except Poll.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)

            poll.opened = False
            poll.save()

            self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))"""