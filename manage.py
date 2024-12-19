#!/usr/bin/env python
import os
import sys
import django
from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model


def initialize():
    """Initialize the database and create a superuser if it doesn't exist."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_online.settings')  # Замените на ваш проект
    django.setup()

    from django.core.management import call_command
    call_command("migrate", interactive=False)
    print("Creating superuser if not exists...")
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
        print("Superuser 'admin' created successfully.")
    else:
        print("Superuser already exists.")


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop_online.settings")  # Замените на ваш проект
    if len(sys.argv) > 1 and sys.argv[1] == "runserver":
        initialize()
    execute_from_command_line(sys.argv)
