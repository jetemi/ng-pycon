from wagtail_modeladmin.options import (ModelAdmin, modeladmin_register)
from .models import StandardPage


class StandardPageAdmin(ModelAdmin):
    model = StandardPage
    menu_label = "Standard Pages"
    menu_icon = "doc-full-inverse"
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("title", "slug", "live", "last_published_at")
    list_filter = ("live",)
    search_fields = ("title", "slug", "intro")


modeladmin_register(StandardPageAdmin) 