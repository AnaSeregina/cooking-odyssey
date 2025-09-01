# render_predeploy.py
import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recipesite.settings")
django.setup()

from django.core.management import call_command
from django.conf import settings
from django.db import connection

print("🔧 Running migrations in pre-deploy...")
call_command("migrate", interactive=False, verbosity=1)

print("📂 Runtime DB:", settings.DATABASES["default"]["NAME"])

print("📋 Recipes app migration status:")
call_command("showmigrations", "recipes")

# Assert that the table exists (helps catch DB path mismatches)
with connection.cursor() as cur:
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='recipes_recipe'")
    row = cur.fetchone()
    exists = bool(row)

print("✅ recipes_recipe table present?" , exists)
if not exists:
    print("❌ recipes_recipe table not found. Check DB_PATH and migrations.", file=sys.stderr)
    sys.exit(1)