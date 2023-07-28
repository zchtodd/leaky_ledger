from django.shortcuts import render
from django.contrib.auth import authenticate, login


def home(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            messages.error(request, "Invalid credentials!")

    return render(request, "leaky_ledger/home.html")
