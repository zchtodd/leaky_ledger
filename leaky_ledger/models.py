from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    name = models.CharField(max_length=200)

    @property
    def balance(self):
        return self.transactions.aggregate(Sum("amount"))["amount__sum"] or 0.00


class Transaction(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="transactions"
    )

    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_transaction = models.DateTimeField()

    def __str__(self):
        return self.description
