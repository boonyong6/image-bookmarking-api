from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from ..models import Post

register = template.Library()  # Registers the module as a tag library.


# Use `name` attribute to register the tag using a different name.
@register.simple_tag
def total_posts():
    return Post.published.count()


# Specifies the template that will be rendered with the returned values (context).
@register.inclusion_tag("blog/post/latest_posts.html")
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}


# Return a QuerySet
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count("comments")).order_by(
        "-total_comments"
    )[:count]


# Function uses a different name to prevent a name clash.
@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
