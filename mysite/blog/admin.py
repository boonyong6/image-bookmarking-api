from django.contrib import admin
from .models import Post


# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "author", "publish", "status"]
    list_filter = ["status", "created", "publish", "author"]
    search_fields = ["title", "body"]  # Search bar
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["author"]  # User lookup widget
    date_hierarchy = "publish"  # Date breadcrumbs (below search bar)
    ordering = ["status", "publish"]  # Overrides the default sort order of the model.
    show_facets = admin.ShowFacets.ALWAYS  # Object counts for each filter.
