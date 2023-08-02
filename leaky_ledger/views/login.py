from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("accounts")
        else:
            messages.error(request, "Username or password is incorrect.")
            return HttpResponseRedirect(reverse("home"))

    return render(request, "registration/login.html")
