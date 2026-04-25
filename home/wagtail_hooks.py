from wagtail_modeladmin.options import (ModelAdmin, modeladmin_register)
from .models import SponsorPage, StandardPage


class StandardPageAdmin(ModelAdmin):
    model = StandardPage
    menu_label = "Standard Pages"
    menu_icon = "doc-full-inverse"
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("title", "slug", "live", "last_published_at")
    list_filter = ("live",)
    search_fields = ("title", "slug", "intro")


class SponsorPageAdmin(ModelAdmin):
    model = SponsorPage
    menu_label = "Sponsor Pages"
    menu_icon = "group"
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("title", "slug", "live", "last_published_at")
    list_filter = ("live",)
    search_fields = ("title", "slug", "hero_headline")


modeladmin_register(StandardPageAdmin)
modeladmin_register(SponsorPageAdmin) 