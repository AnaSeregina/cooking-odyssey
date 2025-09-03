from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Recipe

class RecipeSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Recipe.objects.all()

    def location(self, obj):
        # detail page with a slug field
        return f"/r/{obj.slug}/"

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return ["home", "contact", "nutrition", "about"]

    def location(self, item):
        return reverse(item)