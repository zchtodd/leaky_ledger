from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from leaky_ledger.models import Account, Transaction

from faker import Faker
from datetime import datetime
from decimal import Decimal
import random


class Command(BaseCommand):
    help = "Create random users"

    def add_arguments(self, parser):
        parser.add_argument(
            "total", type=int, help="Indicates the number of users to be created"
        )

    def handle(self, *args, **kwargs):
        total = kwargs["total"]
        fake = Faker()
        for i in range(total):
            first = fake.first_name()
            last = fake.last_name()
            domain = random.choice(["gmail.com", "hotmail.com", "aol.com", "juno.com"])

            username = "".join([first[0], last, str(random.randint(1, 99)).zfill(2)])

            email = "".join(
                [first[0], last, str(random.randint(1, 99)).zfill(2), "@", domain]
            )

            User.objects.create(
                username=username, email=email, password=fake.password()
            )

        for user in User.objects.all():
            account1 = Account.objects.create(user=user, name="Checking")
            account2 = Account.objects.create(user=user, name="Savings")

            Transaction.objects.create(
                account=account1,
                description="Initial Balance",
                amount=Decimal(5000),
                date_of_transaction=datetime.now(),
            )

        self.stdout.write(self.style.SUCCESS(f"Successfully created {total} users"))
