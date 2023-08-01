from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q


def user_lookup(request):
    term = request.GET.get("term", "")
    users = User.objects.filter(Q(email__istartswith=term))
    results = []

    for user in users:
        user_info = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
        results.append(user_info)

    return JsonResponse(results, safe=False)
