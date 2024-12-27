from actions.utils import create_action
from decouple import config
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AbstractUser
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils.html import escape
from django.views.decorators.http import require_POST

from .forms import LoginForm, ProfileEditForm, UserEditForm, UserRegistrationForm
from .models import Contact, Profile

User = get_user_model()


# Unused function (`django.contrib.auth`'s built-in views are used instead).
def user_login(request: HttpRequest):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(  # Verifies the user's credentials.
                request, username=cd["username"], password=cd["password"]
            )
            if user is not None:
                if user.is_active:
                    login(request, user)  # Sets the user in the current session.
                    return HttpResponse("Authenticated successfully")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")
    # GET request
    else:
        form = LoginForm()
    return render(request, "account/login.html", {"form": form})


@login_required
def dashboard(request):
    bookmarklet_launcher = render_to_string(
        "bookmarklet_launcher.js", {"host": config("HOST")}
    )
    bookmarklet_launcher = escape(bookmarklet_launcher)

    return render(
        request,
        "account/dashboard.html",
        {
            "section": "dashboard",
            "bookmarklet_launcher": bookmarklet_launcher,
        },
    )


def register(request: HttpRequest):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet (because we need
            #   to call a separate method to hash and set the password).
            new_user: AbstractUser = user_form.save(commit=False)
            # Set the chosen password.
            new_user.set_password(user_form.cleaned_data["password"])
            # Save the User object.
            new_user.save()
            # Create the user profile.
            Profile.objects.create(user=new_user)
            create_action(new_user, "has created an account.")
            return render(request, "account/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})


@login_required
def edit(request: HttpRequest):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully")
        else:
            messages.error(request, "Error updating your profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "account/edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@login_required
def user_list(request: HttpRequest):
    users = User.objects.filter(is_active=True)
    return render(
        request, "account/user/list.html", {"section": "people", "users": users}
    )


@login_required
def user_detail(request: HttpRequest, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(
        request, "account/user/detail.html", {"section": "people", "user": user}
    )


@require_POST
@login_required
def user_follow(request: HttpRequest):
    user_id = request.POST.get("id")
    action = request.POST.get("action")

    if user_id is None or action is None:
        return JsonResponse({"status": "error"})

    try:
        user = User.objects.get(id=user_id)

        if action == "follow":
            Contact.objects.get_or_create(user_from=request.user, user_to=user)
            create_action(request.user, "is following", user)
        else:
            Contact.objects.filter(user_from=request.user, user_to=user).delete()

        return JsonResponse({"status": "ok"})
    except User.DoesNotExist:
        return JsonResponse({"status": "error"})
