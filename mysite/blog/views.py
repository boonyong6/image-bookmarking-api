from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail

from .forms import EmailPostForm
from .models import Post


# Similar to the `post_list` view. But, exception handling is a bit different.
class PostListView(ListView):
    """
    Alternative post list view.
    """

    # Alternatively, define `model = Post` and Django will built
    #   the generic `Post.objects.all()` QuerySet.
    queryset = Post.published.all()
    context_object_name = "posts"  # Default name is `object_list`.
    paginate_by = 3
    template_name = "blog/post/list.html"  # Default template is `blog/post_list.html`.


# Create your views here.
def post_list(request: HttpRequest):
    post_list = Post.published.all()
    # Pagination with 3 posts per page.
    paginator = Paginator(post_list, 3)
    # Retrieve the HTTP `GET` parameter. (Default: 1st page)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        # If page_number is out of range get last page of results
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # If page_number is not an integer get the first page.
        posts = paginator.page(1)

    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(request, "blog/post/detail.html", {"post": post})


def post_share(request: HttpRequest, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == "POST":
        # Form was submitted
        form = EmailPostForm(request.POST)  # Submitted data.
        if form.is_valid():
            # From fields passed validation.
            cd = form.cleaned_data

            # * Send email
            # To build a complete URL, including the HTTP schema and hostname.
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd["name"]} ({cd["email"]}) recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd["name"]}'s comments: {cd["comments"]}"
            send_mail(
                subject=subject,
                message=message,
                from_email=None,  # Use `DEFAULT_FROM_EMAIL setting`.
                recipient_list=[cd["to"]],
            )
            sent = True
    else:
        form = EmailPostForm()  # Initial form.

    return render(
        request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
    )
