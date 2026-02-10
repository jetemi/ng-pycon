from wagtail_modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register

from .models import Coupon, Ticket, TicketSale, TicketType


class TicketTypeAdmin(ModelAdmin):
    model = TicketType
    menu_label = "Ticket Types"
    menu_icon = "tag"
    menu_order = 100
    add_to_settings_menu = False
    list_display = [
        "name",
        "conference_year",
        "price",
        "early_bird_price",
        "early_bird_count",
        "regular_count",
        "is_active",
        "display_order",
    ]
    list_filter = ["conference_year", "is_active"]
    search_fields = ["name"]
    ordering = ["conference_year", "display_order"]


class CouponAdmin(ModelAdmin):
    model = Coupon
    menu_label = "Coupons"
    menu_icon = "snippet"
    menu_order = 200
    list_display = ["code", "percentage", "max_usage", "expired", "conference_year"]
    list_filter = ["conference_year", "expired"]
    search_fields = ["code"]


class TicketAdmin(ModelAdmin):
    model = Ticket
    menu_label = "Orders"
    menu_icon = "doc-full"
    menu_order = 300
    list_display = [
        "order",
        "user",
        "ticket_type",
        "quantity",
        "amount",
        "status",
        "conference_year",
        "date_created",
    ]
    list_filter = ["status", "conference_year", "ticket_type__name"]
    search_fields = ["order", "user__email"]
    ordering = ["-date_created"]


class TicketSaleAdmin(ModelAdmin):
    model = TicketSale
    menu_label = "Attendees"
    menu_icon = "group"
    menu_order = 400
    list_display = ["full_name", "ticket", "diet", "tagline"]
    list_filter = ["ticket__ticket_type__name", "diet"]
    search_fields = ["full_name", "user__email"]


class TicketsAdminGroup(ModelAdminGroup):
    menu_label = "Tickets"
    menu_icon = "ticket"
    menu_order = 200
    items = (TicketTypeAdmin, CouponAdmin, TicketAdmin, TicketSaleAdmin)


modeladmin_register(TicketsAdminGroup)
