from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

from leaky_ledger.forms.new_user import NewUserForm


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")

        messages.error(request, "Unsuccessful registration. Invalid information.")

    form = NewUserForm()

    return render(
        request=request,
        template_name="leaky_ledger/register.html",
        context={"register_form": form},
    )
