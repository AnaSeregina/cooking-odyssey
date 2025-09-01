# render_predeploy.py
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recipesite.settings")
django.setup()

from django.core.management import call_command
from django.conf import settings

print("Running migrations in pre-deploy...")
call_command("migrate", interactive=False, verbosity=1)
print("Runtime DB:", settings.DATABASES["default"]["NAME"])

print("App migration status:")
call_command("showmigrations", "recipes")