from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    changefreq = "weekly"  # Change frequency of post pages.
    priority = 0.9  # Relevance of post pages in the website. (max: 1)

    def items(self):
        return Post.published.all()  # Objects to include in this sitemap.

    def lastmod(self, obj: Post):
        return obj.updated
