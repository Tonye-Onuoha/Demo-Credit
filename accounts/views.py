from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.contrib import messages
import requests

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            url = f"https://adjutor.lendsqr.com/v2/verification/karma/{email}"
            api_key = "sk_live_52JLXbf8oEixCvuYat1qHUOtmBcjFwFM2NGbpzdG"
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(url, headers=headers)
            json_response = response.json()
            if json_response["message"] == "Identity not found in karma ecosystem":
                user = User(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                )
                user.set_password(password)
                user.save()
                messages.success(
                    request,
                    f"Welcome {first_name}, you have successfully created a new account. Sign in to continue.",
                )
                return redirect(reverse("login"))
            else:
                raise PermissionDenied
    else:
        form = RegisterForm()
    context = {"form": form}
    return render(request, "registration/register.html", context)
