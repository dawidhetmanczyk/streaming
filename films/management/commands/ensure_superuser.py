import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Tworzy superusera z zmiennych srodowiskowych, jesli jeszcze nie istnieje."

    def handle(self, *args, **options):
        username = os.getenv("DJANGO_SUPERUSER_USERNAME", "").strip()
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "").strip()
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "").strip()

        if not username or not password:
            self.stdout.write("Pominieto tworzenie superusera (brak zmiennych srodowiskowych).")
            return

        User = get_user_model()
        if User.objects.filter(username=username).exists():
            self.stdout.write(f"Superuser '{username}' juz istnieje.")
            return

        User.objects.create_superuser(username=username, email=email or f"{username}@example.com", password=password)
        self.stdout.write(self.style.SUCCESS(f"Utworzono superusera '{username}'."))
