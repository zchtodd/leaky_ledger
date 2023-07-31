from datetime import datetime, timedelta
from decimal import Decimal
import random

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

from leaky_ledger.forms.new_user import NewUserForm
from leaky_ledger.models import Account, Transaction
from leaky_ledger.fake_data import descriptions


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            account1 = Account.objects.create(user=user, name="Checking")
            account2 = Account.objects.create(user=user, name="Savings")

            now = datetime.utcnow()

            chosen_descriptions = random.sample(descriptions, 10)
            for i in range(10):
                Transaction.objects.create(
                    account=account1,
                    description=chosen_descriptions[i],
                    amount=-Decimal(random.randrange(1000, 50000)) / 100,
                    date_of_transaction=now - timedelta(days=random.randint(1, 9)),
                )

            Transaction.objects.create(
                account=account1,
                description="Underwater Basket Weavers Ltd.",
                amount=Decimal(5000),
                date_of_transaction=now - timedelta(days=10),
            )

            login(request, user)
            return redirect("accounts")

        messages.error(request, "Unsuccessful registration. Invalid information.")

    form = NewUserForm()

    return render(
        request=request,
        template_name="leaky_ledger/register.html",
        context={"register_form": form},
    )
