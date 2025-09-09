"""
URL configuration for recipesite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# recipesite/urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from django.http import HttpResponse

from django.contrib.sitemaps.views import sitemap
from recipes.sitemaps import RecipeSitemap, StaticViewSitemap  # adjust app name if needed

from django.views.decorators.http import require_GET



def healthz(_request):
    return HttpResponse("ok")


@require_GET
def robots_txt(_request):
    content = "\n".join([
        "User-agent: *",
        "Allow: /",
        "Sitemap: https://www.cookingodyssey.net/sitemap.xml",
    ])
    resp = HttpResponse(content, content_type="text/plain")
    resp["Cache-Control"] = "public, max-age=3600"
    return resp


urlpatterns = [
    path("healthz/", healthz),
    path("admin/", admin.site.urls),
    path("", include("recipes.urls")),
]

sitemaps = {
    "recipes": RecipeSitemap,
    "static": StaticViewSitemap,
}

# Serve user-uploaded media files even if DEBUG=False
urlpatterns += [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps, "protocol": "https"}, name="sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
]




