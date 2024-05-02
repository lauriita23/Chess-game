from django.contrib.auth.models import User
from mychess.models import Player
from django.core.management.base import BaseCommand
from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Command(BaseCommand):
    help = 'Creates a superuser.'
    
    def handle(self, *args, **options):
        if not Player.objects.filter(username='alumnodb').exists():
            User.objects.create_superuser(
                username=getenv('USERNAME'),
                password=getenv('PASSWORD'),
            )
        print('Superuser has been created.')