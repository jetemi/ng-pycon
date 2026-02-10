from django.contrib import admin
from django.db import models

from .models import Coupon, Ticket, TicketSale, TicketType


@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "conference_year",
        "price",
        "early_bird_price",
        "current_price_display",
        "early_bird_count",
        "regular_count",
        "total_sold_display",
        "remaining_display",
        "is_active",
    ]
    list_filter = ["conference_year", "is_active"]
    search_fields = ["name"]
    ordering = ["conference_year", "display_order", "price"]

    def current_price_display(self, obj):
        return obj.current_price

    current_price_display.short_description = "Current Price"

    def total_sold_display(self, obj):
        return obj.total_sold

    total_sold_display.short_description = "Sold"

    def remaining_display(self, obj):
        return obj.remaining_count

    remaining_display.short_description = "Remaining"


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "percentage",
        "max_usage",
        "usage_count_display",
        "expired",
        "conference_year",
    ]
    list_filter = ["conference_year", "expired"]
    search_fields = ["code"]
    actions = ["mark_as_expired"]

    def usage_count_display(self, obj):
        return obj.usage_count

    usage_count_display.short_description = "Times Used"

    @admin.action(description="Mark selected coupons as expired")
    def mark_as_expired(self, request, queryset):
        queryset.update(expired=True)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = [
        "order",
        "user",
        "ticket_type",
        "quantity",
        "amount",
        "total_amount",
        "status",
        "conference_year",
        "date_created",
        "date_paid",
    ]
    list_filter = ["status", "conference_year", "ticket_type__name"]
    search_fields = ["order", "user__email", "user__username"]
    readonly_fields = ["order", "date_created", "date_paid"]
    ordering = ["-date_created"]


@admin.register(TicketSale)
class TicketSaleAdmin(admin.ModelAdmin):
    list_display = [
        "ticket_id_display",
        "full_name",
        "ticket_type_name",
        "diet",
        "tagline",
        "ticket",
        "user_email",
    ]
    list_filter = ["ticket__ticket_type__name", "diet"]
    search_fields = ["full_name", "user__email", "user__username"]
    ordering = ["pk"]

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = "Email"
