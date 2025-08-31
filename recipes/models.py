import re
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify

# Regex to strip leading markers like "1.", "1)", "-", "—", "•", "*"
_BULLET_RE = re.compile(r"^\s*(?:\d+[\.\)]|[•\-–—*]+)\s*")

class Recipe(models.Model):
    # Core
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    # Content (one item/step per line; we'll clean common prefixes)
    ingredients = models.TextField(
        help_text="One ingredient per line (no bullets or numbers needed)"
    )
    steps = models.TextField(
        help_text="One step per line (no numbering needed; numbers will be added on the page)"
    )

    # Media (uploaded file; requires Pillow)
    hero_image = models.ImageField(upload_to="recipes/", blank=True, null=True)

    # URL/id
    slug = models.SlugField(unique=True, blank=True)

    # Serving & time
    servings = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1)]
    )
    serving_display = models.CharField(
        max_length=100,
        blank=True,
        help_text='Shown in lists, e.g. "1 serving", "1 wrap", "4 meatballs"',
    )
    prep_minutes = models.PositiveSmallIntegerField(default=0)
    cook_minutes = models.PositiveSmallIntegerField(default=0)

    # Nutrition (per serving)
    calories_kcal = models.PositiveSmallIntegerField(default=0)
    protein_g = models.PositiveSmallIntegerField(default=0)
    fat_g = models.PositiveSmallIntegerField(default=0)
    carbs_g = models.PositiveSmallIntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    # ---------- Helpers for templates / display ----------

    def _clean_block(self, text: str) -> list[str]:
        """Split text into non-empty lines and strip common bullet/number prefixes."""
        lines = [l.strip() for l in (text or "").splitlines()]
        lines = [l for l in lines if l]  # drop empty lines
        return [_BULLET_RE.sub("", l) for l in lines]

    def ingredient_list(self) -> list[str]:
        return self._clean_block(self.ingredients)

    def step_list(self) -> list[str]:
        return self._clean_block(self.steps)

    # ---------- Model housekeeping ----------

    def save(self, *args, **kwargs):
        # Auto-generate slug once (you can edit it in admin if needed)
        if not self.slug:
            self.slug = slugify(self.title)

        # Auto-fill serving_display if empty
        if not self.serving_display:
            self.serving_display = f"{self.servings} serving" + ("s" if self.servings != 1 else "")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title