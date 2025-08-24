# adminui/admin.py
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.apps import apps as django_apps

# Branding
admin.site.site_header = "Automated Timetable — Admin"
admin.site.site_title  = "Timetable Admin"
admin.site.index_title = "Administration"

# Hide built-ins you don’t want in the sidebar
for model in (User, Group):
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass

# # Optional: only hide Sites if the app is installed
if django_apps.is_installed("django.contrib.sites"):
    Site = django_apps.get_model("sites", "Site")
    if Site:
        try:
            admin.site.unregister(Site)
        except admin.sites.NotRegistered:
            pass
