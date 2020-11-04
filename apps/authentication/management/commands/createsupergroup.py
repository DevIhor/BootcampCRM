"""
Management utility to create super group for superusers.
"""
import sys

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import DEFAULT_DB_ALIAS


class NotRunningInTTYException(Exception):
    pass


PASSWORD_FIELD = 'password'


class Command(BaseCommand):
    help = 'Used to create a group for superusers.'
    requires_migrations_checks = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UserModel = get_user_model()

    def add_arguments(self, parser):
        parser.add_argument('--database', default=DEFAULT_DB_ALIAS,
                            help='Specifies the database to use. Default is "default".')

    def execute(self, *args, **options):
        return super().execute(*args, **options)

    def handle(self, *args, **options):
        database = options['database']
        try:
            self.UserModel._default_manager.db_manager(database).create_superuser_group()
            self.stdout.write("Super Group created successfully.")
        except KeyboardInterrupt:
            self.stderr.write('\nOperation cancelled.')
            sys.exit(1)
        except NotRunningInTTYException:
            self.stdout.write('Superuser creation skipped due to not running in a TTY. You can run '
                              '`manage.py createsuperuser` in your project to create one manually.')
