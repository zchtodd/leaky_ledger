from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def accounts(request):
    accounts = request.user.accounts.all()

    return render(
        request,
        "leaky_ledger/accounts.html",
        context={
            "checking": accounts[0],
            "savings": accounts[1],
            "checking_balance": accounts[0].balance,
            "savings_balance": accounts[1].balance,
        },
    )
