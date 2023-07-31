from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from leaky_ledger.models import Transaction, Account


@login_required
def account(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)

    transactions = Transaction.objects.filter(account=account).order_by(
        "-date_of_transaction"
    )

    balance = transactions.aggregate(Sum("amount"))["amount__sum"] or 0

    context = {
        "user": request.user,
        "account": account,
        "balance": balance,
        "transactions": transactions,
    }

    return render(request, "leaky_ledger/account.html", context)
