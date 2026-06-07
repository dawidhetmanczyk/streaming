from django.conf import settings
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(blank=True, default="")

    def __str__(self) -> str:
        return f"Profil({self.user.username})"


class Kategoria(models.Model):
    nazwa = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Kategorie"
        ordering = ["nazwa"]

    def __str__(self) -> str:
        return self.nazwa


class Film(models.Model):
    tytul = models.CharField(max_length=200)
    opis = models.TextField()
    rok_produkcji = models.PositiveIntegerField()
    gatunek = models.CharField(max_length=100)
    czas_trwania = models.PositiveIntegerField(help_text="Czas trwania w minutach")
    miniatura = models.ImageField(upload_to="posters/", blank=True, null=True)
    plakat_static = models.CharField(
        max_length=200,
        blank=True,
        default="",
        help_text="Sciezka wzgledem katalogu static, np. films/posters/placeholder.svg",
    )
    data_dodania = models.DateTimeField(auto_now_add=True)
    kategorie = models.ManyToManyField(Kategoria, blank=True, related_name="filmy")

    class Meta:
        ordering = ["-data_dodania"]

    def __str__(self) -> str:
        return self.tytul

    def srednia_ocena(self):
        result = self.oceny.aggregate(avg=Avg("wartosc"))
        return result["avg"]

    def liczba_glosow(self):
        return self.oceny.count()

    @property
    def srednia_ocena_wyswietlana(self):
        avg = self.srednia_ocena()
        if avg is None:
            return None
        return round(avg, 1)


class Ulubiony(models.Model):
    uzytkownik = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ulubione"
    )
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="ulubione_wpisy")
    dodano = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["uzytkownik", "film"], name="unique_ulubiony"),
        ]
        ordering = ["-dodano"]

    def __str__(self) -> str:
        return f"{self.uzytkownik} -> {self.film}"


class Ocena(models.Model):
    uzytkownik = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="oceny"
    )
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="oceny")
    wartosc = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    utworzono = models.DateTimeField(auto_now_add=True)
    zmieniono = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["uzytkownik", "film"], name="unique_ocena"),
        ]

    def __str__(self) -> str:
        return f"{self.uzytkownik}: {self.wartosc}/10 -> {self.film}"


class Komentarz(models.Model):
    uzytkownik = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="komentarze"
    )
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="komentarze")
    tresc = models.TextField()
    utworzono = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-utworzono"]

    def __str__(self) -> str:
        return f"Komentarz({self.uzytkownik} -> {self.film})"


class HistoriaOgladania(models.Model):
    uzytkownik = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="historia_ogladania"
    )
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="historia_wpisy")
    obejrzano = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Historia ogladania"
        constraints = [
            models.UniqueConstraint(fields=["uzytkownik", "film"], name="unique_historia"),
        ]
        ordering = ["-obejrzano"]

    def __str__(self) -> str:
        return f"{self.uzytkownik} obejrzal {self.film}"


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance: CustomUser, created: bool, **kwargs):
    if created:
        Profile.objects.create(user=instance)
