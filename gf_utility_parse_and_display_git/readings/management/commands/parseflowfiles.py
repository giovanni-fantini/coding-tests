from django.core.management.base import BaseCommand, CommandError
import os
from readings.utils import import_flowfile

class Command(BaseCommand):
    help = 'Parses one or more provided D0010 flow file(s) and imports readings into the app'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('filepaths', nargs='+', type=str, help= 'Full paths to D0010 files')

    def handle(self, *args, **options):
        paths = options['filepaths']
        for path in paths:
            if not os.path.isfile(path):
                raise CommandError(f'{path} is not a path to a valid file')
            
            import_flowfile(path)
            
        self.stdout.write(f'Task succesfully executed: {len(paths)} flow files processed')