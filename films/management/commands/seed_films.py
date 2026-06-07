from django.core.management.base import BaseCommand

from films.models import Film, Kategoria


class Command(BaseCommand):
    help = "Tworzy przykladowe kategorie i filmy demo."

    def handle(self, *args, **options):
        categories = {
            "Akcja": ["Neonowy Pościg", "Ostatni Kontrakt"],
            "Dramat": ["Ciche Morze", "Powrót do Domu"],
            "Komedia": ["Przypadkowy Bohater"],
            "Sci-Fi": ["Neonowy Pościg", "Gwiezdny Most"],
        }

        kategoria_objs = {}
        for name in categories:
            kategoria_objs[name], _ = Kategoria.objects.get_or_create(nazwa=name)

        films_data = [
            {
                "tytul": "Neonowy Pościg",
                "opis": "Futurystyczny thriller akcji o kierowcy, który musi ocalić miasto przed cyber-zagrożeniem.",
                "rok_produkcji": 2024,
                "gatunek": "Sci-Fi",
                "czas_trwania": 118,
                "plakat_static": "films/posters/poster1.svg",
                "kategorie": ["Akcja", "Sci-Fi"],
            },
            {
                "tytul": "Ciche Morze",
                "opis": "Intymna opowieść o rodzinie wracającej do nadmorskiego miasteczka po latach.",
                "rok_produkcji": 2022,
                "gatunek": "Dramat",
                "czas_trwania": 104,
                "plakat_static": "films/posters/poster2.svg",
                "kategorie": ["Dramat"],
            },
            {
                "tytul": "Przypadkowy Bohater",
                "opis": "Lekka komedia o nieśmiałym urzędniku, który przypadkiem staje się lokalną legendą.",
                "rok_produkcji": 2021,
                "gatunek": "Komedia",
                "czas_trwania": 96,
                "plakat_static": "films/posters/poster3.svg",
                "kategorie": ["Komedia"],
            },
            {
                "tytul": "Ostatni Kontrakt",
                "opis": "Emerytowany agent wraca do gry, gdy jego dawny partner znika bez śladu.",
                "rok_produkcji": 2023,
                "gatunek": "Akcja",
                "czas_trwania": 112,
                "plakat_static": "films/posters/poster4.svg",
                "kategorie": ["Akcja"],
            },
            {
                "tytul": "Gwiezdny Most",
                "opis": "Ekipa odkrywców przemierza nieznaną galaktykę w poszukiwaniu nowego domu dla ludzkości.",
                "rok_produkcji": 2025,
                "gatunek": "Sci-Fi",
                "czas_trwania": 132,
                "plakat_static": "films/posters/poster5.svg",
                "kategorie": ["Sci-Fi"],
            },
            {
                "tytul": "Powrót do Domu",
                "opis": "Poruszający dramat o bracie i siostrze, którzy po latach spotykają się na pogrzebie ojca.",
                "rok_produkcji": 2020,
                "gatunek": "Dramat",
                "czas_trwania": 101,
                "plakat_static": "films/posters/poster2.svg",
                "kategorie": ["Dramat"],
            },
            {
                "tytul": "Cienie Metropolii",
                "opis": "Detektyw tropi serię tajemniczych zniknięć w wielkomiejskim labiryncie ulic.",
                "rok_produkcji": 2019,
                "gatunek": "Kryminał",
                "czas_trwania": 109,
                "plakat_static": "films/posters/poster4.svg",
                "kategorie": ["Akcja", "Dramat"],
            },
            {
                "tytul": "Letni Koncert",
                "opis": "Młoda muzyk walczy o wielki debiut podczas letniego festiwalu nad jeziorem.",
                "rok_produkcji": 2018,
                "gatunek": "Dramat",
                "czas_trwania": 98,
                "plakat_static": "films/posters/poster3.svg",
                "kategorie": ["Dramat", "Komedia"],
            },
            {
                "tytul": "Robot i Ja",
                "opis": "Ciepła opowieść o przyjaźni nastolatka z domowym androidem.",
                "rok_produkcji": 2024,
                "gatunek": "Sci-Fi",
                "czas_trwania": 105,
                "plakat_static": "films/posters/poster1.svg",
                "kategorie": ["Sci-Fi", "Komedia"],
            },
            {
                "tytul": "Granica Północy",
                "opis": "Ekspedycja ratunkowa w arktycznej dziczy staje przed niemożliwym wyborem.",
                "rok_produkcji": 2017,
                "gatunek": "Przygodowy",
                "czas_trwania": 114,
                "plakat_static": "films/posters/poster5.svg",
                "kategorie": ["Akcja", "Dramat"],
            },
            {
                "tytul": "Miasto Nocą",
                "opis": "Kronika kilku losów splatających się podczas jednej burzliwej nocy w centrum miasta.",
                "rok_produkcji": 2016,
                "gatunek": "Dramat",
                "czas_trwania": 102,
                "plakat_static": "films/posters/poster2.svg",
                "kategorie": ["Dramat"],
            },
            {
                "tytul": "Plan B",
                "opis": "Grupa przyjaciół realizuje szalony plan, aby uratować lokalne kino przed zamknięciem.",
                "rok_produkcji": 2023,
                "gatunek": "Komedia",
                "czas_trwania": 94,
                "plakat_static": "films/posters/poster3.svg",
                "kategorie": ["Komedia"],
            },
            {
                "tytul": "Echo Przeszłości",
                "opis": "Historyczny dramat o archiwistce odkrywającej listy z czasów wojny.",
                "rok_produkcji": 2015,
                "gatunek": "Dramat",
                "czas_trwania": 121,
                "plakat_static": "films/posters/poster4.svg",
                "kategorie": ["Dramat"],
            },
        ]

        created_count = 0
        for data in films_data:
            kategorie_names = data.pop("kategorie")
            film, created = Film.objects.update_or_create(
                tytul=data["tytul"],
                defaults=data,
            )
            film.kategorie.set([kategoria_objs[name] for name in kategorie_names])
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed zakonczony. Utworzono {created_count} nowych filmow, lacznie {Film.objects.count()} w bazie."
            )
        )
