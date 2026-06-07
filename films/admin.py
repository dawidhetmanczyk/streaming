from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    CustomUser,
    Film,
    HistoriaOgladania,
    Kategoria,
    Komentarz,
    Ocena,
    Profile,
    Ulubiony,
)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "is_staff", "date_joined")
    search_fields = ("username", "email")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "bio")


@admin.register(Kategoria)
class KategoriaAdmin(admin.ModelAdmin):
    search_fields = ("nazwa",)


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ("tytul", "rok_produkcji", "gatunek", "czas_trwania", "data_dodania")
    list_filter = ("gatunek", "rok_produkcji", "kategorie")
    search_fields = ("tytul", "opis", "gatunek")
    filter_horizontal = ("kategorie",)
    readonly_fields = ("data_dodania",)


admin.site.register(Ulubiony)
admin.site.register(Ocena)
admin.site.register(Komentarz)
admin.site.register(HistoriaOgladania)
