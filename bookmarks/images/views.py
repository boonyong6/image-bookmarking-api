import redis
from actions.utils import create_action
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, JsonResponse
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from bookmarks.typing import settings

from .forms import ImageCreateForm
from .models import Image

# Connect to redis
r = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


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
            create_action(request.user, "bookmarked image", new_image)
            messages.success(request, "Image added successfully")
            # Redirect to new created item detail view.
            return redirect(new_image.get_absolute_url())
    else:
        # Build form with data provided by the bookmarklet via GET.
        form = ImageCreateForm(data=request.GET)

    return render(
        request, "images/image/create.html", {"section": "images", "form": form}
    )


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # Increment total image views by 1.
    total_views = r.incr(f"image:{image.id}:views")
    # Increment image ranking by 1.
    r.zincrby("image_ranking", 1, image.id)
    return render(
        request,
        "images/image/detail.html",
        {"section": "images", "image": image, "total_views": total_views},
    )


@login_required
@require_POST
def image_like(request: HttpRequest):
    image_id = request.POST.get("id")
    action = request.POST.get("action")
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == "like":
                image.users_like.add(request.user)
                create_action(request.user, "likes", image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({"status": "ok"})
        except Image.DoesNotExist:
            pass
    return JsonResponse({"status": "error"})


@login_required
def image_list(request: HttpRequest):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get("page")
    images_only = request.GET.get("images_only")  # Flag to distinguish AJAX.

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page.
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            # If AJAX request and page out of range return an empty page.
            return HttpResponse("")
        # If page out of range return last page of results.
        images = paginator.page(paginator.num_pages)

    if images_only:
        return render(
            request,
            "images/image/list_images.html",
            {"section": "images", "images": images},
        )

    return render(
        request,
        "images/image/list.html",
        {"section": "images", "images": images},
    )


@login_required
def image_ranking(request):
    # * Get image ranking dictionary.
    # `start=0` specifies the lowest score. `end=-1` specifies the highest score.
    #   Range of 0 to -1 returns all elements.
    image_ranking_list: list[tuple[bytes, int]] = r.zrange(
        "image_ranking",
        start=0,
        end=-1,
        desc=True,
        withscores=True,
        score_cast_func=int,
    )[:10]
    image_ranking = {int(key): value for key, value in image_ranking_list}
    image_ranking_ids = list(image_ranking)
    # * Get most viewed images.
    # Force query to be executed using `list()`.
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    # Sort by index of appearance in the image ranking.
    most_viewed.sort(key=lambda image: image_ranking_ids.index(image.id))
    for image in most_viewed:
        image.views = image_ranking.get(image.id)

    return render(
        request,
        "images/image/ranking.html",
        {"section": "images", "most_viewed": most_viewed},
    )
