"""
Register Travel Grant models with Wagtail admin.
"""

from wagtail_modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from .models import (
    GrantReviewerAssignment,
    GrantReviewerProfile,
    GrantSettings,
    TravelGrantApplication,
    TravelGrantPayment,
)


class GrantSettingsAdmin(ModelAdmin):
    model = GrantSettings
    menu_label = "Grant Settings"
    menu_icon = "cog"
    menu_order = 100
    list_display = [
        "conference_year",
        "status",
        "application_deadline",
        "max_grant_budget",
        "max_per_applicant",
    ]
    list_filter = ["status"]
    ordering = ["-conference_year"]


class TravelGrantApplicationAdmin(ModelAdmin):
    model = TravelGrantApplication
    menu_label = "Applications"
    menu_icon = "doc-full"
    menu_order = 200
    list_display = [
        "user",
        "conference_year",
        "status",
        "country_of_residence",
        "total_requested_display",
        "submitted_at",
    ]
    list_filter = ["status", "conference_year"]
    search_fields = ["user__email", "user__first_name", "user__last_name"]
    ordering = ["-created_at"]

    def total_requested_display(self, obj):
        return f"₦{obj.total_requested:,.2f}"

    total_requested_display.short_description = "Total Requested"


class GrantReviewerProfileAdmin(ModelAdmin):
    model = GrantReviewerProfile
    menu_label = "Reviewers"
    menu_icon = "group"
    menu_order = 300
    list_display = ["user", "is_chair", "is_finance", "is_active"]
    list_filter = ["is_chair", "is_finance", "is_active"]


class GrantReviewerAssignmentAdmin(ModelAdmin):
    model = GrantReviewerAssignment
    menu_label = "Assignments"
    menu_icon = "tasks"
    menu_order = 350
    list_display = ["reviewer", "application", "has_conflict", "assigned_at"]
    list_filter = ["has_conflict"]
    search_fields = ["reviewer__user__email", "application__user__email"]


class TravelGrantPaymentAdmin(ModelAdmin):
    model = TravelGrantPayment
    menu_label = "Payments"
    menu_icon = "form"
    menu_order = 400
    list_display = ["application", "payment_status", "amount_paid", "reference", "paid_at"]


class GrantsAdminGroup(ModelAdminGroup):
    menu_label = "Travel Grants"
    menu_icon = "form"
    menu_order = 250
    items = (
        GrantSettingsAdmin,
        TravelGrantApplicationAdmin,
        GrantReviewerProfileAdmin,
        GrantReviewerAssignmentAdmin,
        TravelGrantPaymentAdmin,
    )


modeladmin_register(GrantsAdminGroup)
