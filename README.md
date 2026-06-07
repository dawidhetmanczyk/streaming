# StreamFlix — Platforma Streamingowa w Django

Projekt zaliczeniowy z przedmiotu **Aplikacje internetowe w Django** (Temat 5: Strona z Filmami / Streaming).

**Autor:** Dawid Hetmańczyk

## Link do aplikacji (serwer)

**https://streaming-platform-cp2i.onrender.com**

Repozytorium GitHub: **https://github.com/dawidhetmanczyk/streaming**

## Opis

StreamFlix to prosta platforma streamingowa inspirowana serwisami VOD (Netflix, HBO Max). Umożliwia przeglądanie katalogu filmów, wyszukiwanie, ocenianie, komentowanie oraz zarządzanie ulubionymi i historią oglądania.

Niezalogowany użytkownik może przeglądać publiczne treści (strona główna, wyszukiwarka, szczegóły filmów). Po zalogowaniu dostępne są ulubione, oceny, komentarze i historia oglądania.

## Wymagania zaliczenia (11 punktów)

| # | Wymaganie | Realizacja |
|---|-----------|------------|
| 1 | Rejestracja, logowanie, wylogowanie, edycja profilu | `/register/`, `/login/`, `/logout/`, `/profil/` |
| 2 | Model Film (tytuł, opis, rok, gatunek, czas, miniatura, data dodania) | model `Film` w `films/models.py` |
| 3 | Strona główna (najnowsze, wyszukiwarka, lista filmów) | `/` |
| 4 | Szczegóły filmu | `/film/<id>/` |
| 5 | Wyszukiwanie po tytule i gatunku | `/szukaj/` |
| 6 | Panel administratora Django (CRUD filmów) | `/admin/` |
| 7 | Lista ulubionych | `/ulubione/` |
| 8 | Oceny 1–10 ze średnią i liczbą głosów | formularz na stronie szczegółów filmu |
| 9 | Model Kategoria (M2M z Film) | model `Kategoria`, filtrowanie na stronie głównej |
| 10 | Komentarze (dodawanie, usuwanie własnych) | sekcja komentarzy na stronie filmu |
| 11 | Historia oglądania | zapis przy wejściu w szczegóły, widok `/historia/` |

## Rozszerzenia projektu zaliczeniowego

- filtrowanie filmów po kategoriach na stronie głównej
- sekcja „Najwyżej oceniane”
- paginacja listy filmów (12 na stronę)
- komenda `seed_films` z przykładowymi danymi demo
- walidacja formularzy ocen i komentarzy

## Technologie

- Python 3.12+
- Django 5.2
- SQLite (lokalnie) / PostgreSQL (Render)
- Bootstrap 5 + własny CSS
- WhiteNoise, Gunicorn
- Hosting: Render.com

## Panel administratora

- URL: **https://streaming-platform-cp2i.onrender.com/admin/**
- Login: `admin`
- Hasło: wygenerowane przez Render (Environment → `DJANGO_SUPERUSER_PASSWORD`)

W panelu admin można dodawać, edytować i usuwać filmy oraz kategorie.

## Instalacja lokalna

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_films
python manage.py createsuperuser
python manage.py runserver
```

Aplikacja: http://127.0.0.1:8000/

## Struktura projektu

```
streaming_platform/   — konfiguracja Django
films/                — modele, widoki, formularze, admin
templates/            — szablony HTML
static/               — CSS i plakaty demo
build.sh, render.yaml — wdrożenie na Render
```

## Oddanie na Moodle

Archiwum: `django_streaming_submission.zip` (generowane poleceniem `python make_submission_zip.py`).

Link do aplikacji: `link_zaliczenie.txt`
