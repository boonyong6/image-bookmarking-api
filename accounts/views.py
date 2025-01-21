from typing import cast

from decouple import config
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AbstractUser
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.html import escape
from django.views.decorators.http import require_POST
from oauth2_provider.views.generic import ProtectedResourceView

from actions.models import Action
from actions.utils import create_action

from .forms import LoginForm, ProfileEditForm, UserEditForm, UserRegistrationForm
from .models import Contact

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
    return render(request, "accounts/login.html", {"form": form})


@login_required
def dashboard(request):
    bookmarklet_launcher = render_to_string(
        "bookmarklet_launcher.js", {"host": config("HOST")}
    )
    bookmarklet_launcher = escape(bookmarklet_launcher)

    # Display all actions by default.
    actions = Action.objects.exclude(user=request.user)
    following_ids = cast(QuerySet, request.user.following).values_list("id", flat=True)
    if following_ids:
        # If user is following others, retrieve only their actions.
        actions = actions.filter(user_id__in=following_ids)
    # Eager loading `user` and `user__profile` related objects.
    actions = actions.select_related("user", "user__profile").prefetch_related(
        "target"
    )[:10]

    return render(
        request,
        "accounts/dashboard.html",
        {
            "section": "dashboard",
            "bookmarklet_launcher": bookmarklet_launcher,
            "actions": actions,
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
            # ! Create profile and action will be handled by `post_save` signals.
            # # Create the user profile.
            # Profile.objects.create(user=new_user)
            # create_action(new_user, "has created an account.")
            return render(
                request,
                "accounts/register_done.html",
                {"new_user": new_user, "next": request.GET.get("next", None)},
            )
    else:
        user_form = UserRegistrationForm()

    return render(request, "accounts/register.html", {"user_form": user_form})


@login_required
def user_edit(request: HttpRequest):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save()
            messages.success(request, "Profile updated successfully")
            return redirect(profile)
        else:
            messages.error(request, "Error updating your profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "accounts/edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@login_required
def user_list(request: HttpRequest):
    users = User.objects.filter(is_active=True)
    return render(
        request, "accounts/user/list.html", {"section": "people", "users": users}
    )


@login_required
def user_detail(request: HttpRequest, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(
        request, "accounts/user/detail.html", {"section": "people", "user": user}
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


class ApiEndpoint(ProtectedResourceView):
    def get(self, request: HttpRequest, *args, **kwargs):
        print(f"{request.user=}")
        if hasattr(request, "access_token"):
            print(f"{request.access_token=}")
        return HttpResponse("Hello, OAuth2!")


@login_required
def secret_page(request, *args, **kwargs):
    return HttpResponse("Secret contents!", status=200)
