from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login
from django.contrib import messages


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            messages.success(request, "Registration successful.")
            return redirect("home")
        else:
            return render(request, "registration/signup.html", {"form": form})
    else:
        form = SignUpForm()
        return render(request, "registration/signup.html", {"form": form})
