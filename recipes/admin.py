from django.contrib import admin

# Register your models here.

from .models import Recipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "calories_kcal", "protein_g", "fat_g", "carbs_g", "serving_display", "created_at")
    list_filter = ("created_at",)
    search_fields = ("title", "subtitle", "ingredients", "description")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ("Basic Info", {"fields": ("title", "subtitle", "description", "slug", "hero_image")}),
        ("Recipe Content", {"fields": ("ingredients", "steps")}),
        ("Time & Servings", {"fields": ("servings", "serving_display", "prep_minutes", "cook_minutes")}),
        ("Nutrition Facts (per serving)", {"fields": ("calories_kcal", "protein_g", "fat_g", "carbs_g")}),
        ("Meta", {"fields": ("created_at",), "classes": ("collapse",)}),
    )
    readonly_fields = ("created_at",)
