from django.contrib import admin

from scrape_app.models import WebPage, Tag

# Register your models here.
admin.site.register(WebPage)
admin.site.register(Tag)
