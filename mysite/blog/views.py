from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity
from taggit.models import Tag

from .forms import CommentForm, EmailPostForm, SearchForm
from .models import Comment, Post


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
def post_list(request: HttpRequest, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        # Use a list and the `__in` field lookup to filter posts by tags
        # Many-to-many relationship -
        #   One post can have many tags and one tag can be related to many posts.
        post_list = post_list.filter(tags__in=[tag])

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

    return render(request, "blog/post/list.html", {"posts": posts, "tag": tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    # List of active comments for this post.
    comments = post.comments.filter(active=True)
    # Form for users to comment.
    form = CommentForm()

    # * List of similar posts
    # A QuerySet that returns a list of IDs.
    # Pass `flat=True` to get single values such as [1, 2, 3, ...]
    #   instead of [(1,) (2,) (3,) ...].
    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:4]
    # # Alternative: Provided by `django-taggit` (not QuerySet, not lazy).
    # similar_posts = post.tags.similar_objects()

    return render(
        request,
        "blog/post/detail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
            "similar_posts": similar_posts,
        },
    )


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
            subject = f"{cd['name']} ({cd['email']}) recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"
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


@require_POST
def post_comment(request: HttpRequest, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment: Comment = None

    # A comment was posted.
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database.
        comment = form.save(commit=False)
        # Assign the post to the comment.
        comment.post = post
        # Save the comment to the database.
        comment.save()

    return render(
        request,
        "blog/post/comment.html",
        {"post": post, "form": form, "comment": comment},
    )


def post_search(request: HttpRequest):
    form = SearchForm()
    query = None
    results = []

    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            results = (
                Post.published.annotate(similarity=TrigramSimilarity("title", query))
                .filter(similarity__gt=0.1)
                .order_by("-similarity")
            )

    return render(
        request,
        "blog/post/search.html",
        {"form": form, "query": query, "results": results},
    )
