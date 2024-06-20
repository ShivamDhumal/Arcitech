import json
from django.core.management.base import BaseCommand
from cms_app.models import CustomUser  
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User



class Command(BaseCommand):
    help = 'Seed superuser from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **options):
        json_file = options['json_file']
        User = get_user_model()  

        try:
            with open(json_file, 'r') as file:
                data = json.load(file)

            for user_data in data:
                if user_data.get('model') == 'auth.user':
                    fields = user_data.get('fields', {})
                    username = fields.get('username')
                    password = fields.get('password')
                    email = fields.get('email')

                    if username and password:
                        user, created = User.objects.get_or_create(
                            username=username,
                            email=email,
                            is_superuser=fields.get('is_superuser', False),
                            is_staff=fields.get('is_staff', False),
                            is_active=fields.get('is_active', True),
                        )
                        user.set_password(password)
                        user.save()

                        self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))
                    else:
                        self.stderr.write(self.style.ERROR('Username and password are required for creating a superuser.'))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'File not found: {json_file}'))
