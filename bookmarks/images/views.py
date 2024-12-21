from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.shortcuts import redirect, render

from .forms import ImageCreateForm


@login_required
def image_create(request: HttpRequest):
    if request.method == "POST":
        # Form is sent.
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            # Assign current user to the object.
            new_image.user = request.user
            new_image.save()
            messages.success(request, "Image added successfully")
            # Redirect to new created item detail view.
            return redirect(new_image.get_absolute_url())
    else:
        # Build form with data provided by the bookmarklet via GET.
        form = ImageCreateForm(data=request.GET)

    return render(
        request, "images/image/create.html", {"section": "images", "form": form}
    )
