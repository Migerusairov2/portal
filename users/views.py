from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomPasswordChangeForm



def cancel_password_setup(request):
    return redirect("account_logout")


@login_required
def change_password(request):

    if request.method == "POST":
        form = CustomPasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():
            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            messages.success(
                request,
                "Password updated successfully."
            )

            return redirect("profile")

    else:
        form = CustomPasswordChangeForm(request.user)

    return render(
        request,
        "account/change_password.html",
        {
            "form": form
        }
    )


@login_required
def set_password(request):
    if request.method == "POST":
        form = SetPasswordForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            return redirect("profile")

    else:

        form = SetPasswordForm(request.user)


    return render(
        request,
        "account/set_password.html",
        {
            "form": form
        }
    )