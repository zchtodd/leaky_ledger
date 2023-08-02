import json
import time

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from leaky_ledger.models import Account, Transaction


@login_required
@csrf_exempt
def external_transfer(request):
    if request.method != "POST":
        return HttpResponseBadRequest()

    try:
        data = json.loads(request.body)
    except ValueError:
        return JsonResponse({"message": "Invalid JSON"}, status=400)

    source_account_name = data.get("sourceAccount", "").lower()
    destination_email = data.get("destinationEmail", "").lower()
    transfer_amount = data.get("transferAmount")

    if not source_account_name:
        return JsonResponse({"message": "Please select source account."}, status=400)

    if not destination_email:
        return JsonResponse({"message": "Please select destination email."}, status=400)

    if not transfer_amount:
        return JsonResponse({"message": "Invalid transfer amount."}, status=400)

    transfer_amount = Decimal(transfer_amount)

    source_account = get_object_or_404(
        Account, name__iexact=source_account_name, user=request.user
    )

    try:
        destination_user = get_user_model().objects.get(email__iexact=destination_email)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "Invalid destination email."}, status=400)

    destination_account = Account.objects.get(user=destination_user, name="Checking")

    if source_account.balance < transfer_amount:
        return JsonResponse({"message": "Insufficient balance."}, status=400)

    # Intentionally allowing negatives here as a vulnerability but we don't want
    # exploitation of this to overdraw the attacked account.
    if transfer_amount < 0 and destination_account.balance < abs(transfer_amount):
        return JsonResponse({"message": "Insufficient balance."}, status=400)

    source_transaction = Transaction(
        account=source_account,
        description=f"Transfer to {destination_email} account",
        amount=-transfer_amount,
        date_of_transaction=timezone.now(),
    )

    destination_transaction = Transaction(
        account=destination_account,
        description=f"Received from {source_account_name} account",
        amount=transfer_amount,
        date_of_transaction=timezone.now(),
    )

    time.sleep(0.5)

    source_transaction.save()
    destination_transaction.save()

    return JsonResponse({"message": "Transfer completed successfully"}, status=200)
