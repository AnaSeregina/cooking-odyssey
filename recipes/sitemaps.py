from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Recipe

class RecipeSitemap(Sitemap):
    changefreq = "monthly"   # recipes rarely change
    priority = 0.8

    def items(self):
        return Recipe.objects.all()

    def location(self, obj):
        return reverse("recipe_detail", args=[obj.slug])


class StaticViewSitemap(Sitemap):
    def items(self):
        return ["home", "nutrition", "about", "contact"]

    def location(self, item):
        return reverse(item)

    def changefreq(self, item):
        if item == "home":
            return "daily"   # homepage changes often
        elif item == "nutrition":
            return "weekly"  # updates with new recipes
        else:
            return "yearly"  # about/contact rarely change

    def priority(self, item):
        if item == "home":
            return 1.0
        elif item == "nutrition":
            return 0.7
        else:
            return 0.5