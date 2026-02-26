from datetime import date, time, timedelta

from django.core.management.base import BaseCommand

from ...models import Hall, Performance, Play, Theatre


class Command(BaseCommand):
    help = "Creates sample theatre data (theatres, plays, halls, and performances)"

    def handle(self, *args, **options):
        self.stdout.write("Creating sample data...")

        # Create Theatres
        theatre1, created = Theatre.objects.get_or_create(
            name="Национален театър 'Иван Вазов'",
            defaults={
                "city": "София",
                "address": "ул. Драган Цанков 2, 1000 София",
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created theatre: {theatre1.name}"))

        theatre2, created = Theatre.objects.get_or_create(
            name="Театър 'Българска армия'",
            defaults={
                "city": "София",
                "address": "ул. Раковски 98, 1000 София",
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created theatre: {theatre2.name}"))

        theatre3, created = Theatre.objects.get_or_create(
            name="Младежки театър",
            defaults={
                "city": "София",
                "address": "ул. Раковски 108, 1000 София",
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created theatre: {theatre3.name}"))

        # Create Halls
        hall1, created = Hall.objects.get_or_create(
            name="Главна зала",
            theatre=theatre1,
            defaults={"capacity": 550},
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created hall: {hall1.name}"))

        hall2, created = Hall.objects.get_or_create(
            name="Малка сцена",
            theatre=theatre1,
            defaults={"capacity": 200},
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created hall: {hall2.name}"))

        hall3, created = Hall.objects.get_or_create(
            name="Главна зала",
            theatre=theatre2,
            defaults={"capacity": 400},
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created hall: {hall3.name}"))

        # Create Plays
        play1, created = Play.objects.get_or_create(
            title="Хамлет",
            defaults={
                "description": "Класическа трагедия на Уилям Шекспир за принца на Дания.",
                "duration_minutes": 180,
                "theatre": theatre1,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created play: {play1.title}"))

        play2, created = Play.objects.get_or_create(
            title="Ромео и Жулиета",
            defaults={
                "description": "Великата любовна история на Шекспир.",
                "duration_minutes": 150,
                "theatre": theatre1,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created play: {play2.title}"))

        play3, created = Play.objects.get_or_create(
            title="Под игото",
            defaults={
                "description": "Адаптация на романа на Иван Вазов за Априлското въстание.",
                "duration_minutes": 120,
                "theatre": theatre2,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created play: {play3.title}"))

        play4, created = Play.objects.get_or_create(
            title="Снежанка и седемте джуджета",
            defaults={
                "description": "Детска пиеса по приказката на Братя Грим.",
                "duration_minutes": 90,
                "theatre": theatre3,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created play: {play4.title}"))

        # Create Performances (upcoming dates)
        today = date.today()
        performances_data = [
            # Hamlet performances
            (play1, hall1, today + timedelta(days=3), time(19, 0)),
            (play1, hall1, today + timedelta(days=10), time(19, 0)),
            (play1, hall1, today + timedelta(days=17), time(19, 0)),
            # Romeo and Juliet performances
            (play2, hall2, today + timedelta(days=5), time(18, 30)),
            (play2, hall2, today + timedelta(days=12), time(18, 30)),
            # Under the Yoke performances
            (play3, hall3, today + timedelta(days=7), time(19, 30)),
            (play3, hall3, today + timedelta(days=14), time(19, 30)),
            # Snow White performances
            (play4, hall1, today + timedelta(days=1), time(11, 0)),
            (play4, hall1, today + timedelta(days=8), time(11, 0)),
            (play4, hall1, today + timedelta(days=15), time(11, 0)),
        ]

        created_count = 0
        for play, hall, perf_date, perf_time in performances_data:
            performance, created = Performance.objects.get_or_create(
                play=play,
                hall=hall,
                date=perf_date,
                time=perf_time,
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully created {created_count} performances!"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                "\nSample data created successfully! You can now see the cards on the homepage."
            )
        )

