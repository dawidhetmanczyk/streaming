# StreamFlix — Platforma Streamingowa w Django

Projekt zaliczeniowy z przedmiotu **Aplikacje internetowe w Django** (Temat 5: Strona z Filmami / Streaming).

Autor: Dawid Hetmańczyk

## Opis

StreamFlix to prosta platforma streamingowa inspirowana serwisami VOD. Umożliwia przeglądanie katalogu filmów, wyszukiwanie, ocenianie, komentowanie oraz zarządzanie ulubionymi i historią oglądania.

## Wymagania zaliczenia (11 punktów)

1. **System użytkowników** — rejestracja, logowanie, wylogowanie, edycja profilu (awatar, bio)
2. **Model Film** — tytuł, opis, rok produkcji, gatunek, czas trwania, miniatura, data dodania
3. **Strona główna** — najnowsze filmy, wyszukiwarka, lista wszystkich filmów
4. **Szczegóły filmu** — pełny opis, plakat, gatunek, rok, czas trwania
5. **Wyszukiwarka** — po tytule i gatunku
6. **Panel administratora Django** — dodawanie, edycja, usuwanie filmów
7. **Lista ulubionych** — dodawanie, usuwanie, wyświetlanie
8. **Oceny 1–10** — średnia ocena i liczba głosów przy każdym filmie
9. **Kategorie** — model `Kategoria`, relacja M2M z filmem
10. **Komentarze** — dodawanie i usuwanie własnych komentarzy
11. **Historia oglądania** — zapis przy wejściu w szczegóły filmu + widok listy

## Rozszerzenia projektu zaliczeniowego

- filtrowanie filmów po kategoriach na stronie głównej
- sekcja „Najwyżej oceniane”
- paginacja listy filmów (12 na stronę)
- komenda `seed_films` z przykładowymi danymi demo
- walidacja formularzy ocen i komentarzy

## Technologie

- Python 3.12+
- Django 5.2
- SQLite (lokalnie)
- PostgreSQL (Render — produkcja)
- Bootstrap 5 + własny CSS

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

Panel admin: http://127.0.0.1:8000/admin/

## Konta testowe

Po instalacji utwórz konto użytkownika przez `/register/` oraz superusera poleceniem `createsuperuser` do panelu administracyjnego.

## Wdrożenie na Render

1. Utwórz repozytorium Git i wypchnij kod projektu.
2. W Render wybierz **New → Blueprint** i wskaż `render.yaml`.
3. Ustaw w Render zmienne `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD` (w `render.yaml` są już zdefiniowane — hasło generuje Render).
4. Dane demo ładują się automatycznie podczas build (`seed_films`), superuser tworzy komenda `ensure_superuser`.
5. Publiczny URL zapisz w pliku `link_zaliczenie.txt`.

## Struktura projektu

- `streaming_platform/` — konfiguracja Django
- `films/` — modele, widoki, formularze, panel admin
- `templates/` — szablony HTML
- `static/` — CSS i plakaty demo
- `build.sh`, `render.yaml` — konfiguracja wdrożenia

## Oddanie na Moodle

```bash
python make_submission_zip.py
```

Wygeneruje plik `django_streaming_submission.zip` z kodem i dokumentacją (bez bazy i plików tymczasowych).

## Link do aplikacji

Zobacz plik [`link_zaliczenie.txt`](link_zaliczenie.txt).
