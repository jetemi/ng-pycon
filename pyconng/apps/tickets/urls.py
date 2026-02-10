from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = "tickets"

urlpatterns = [
    # Ticket listing
    path("", views.TicketHomeView.as_view(), name="home"),
    # Purchase flow
    path(
        "purchase/",
        csrf_exempt(views.PurchaseView.as_view()),
        name="purchase",
    ),
    path("coupons/", views.valid_coupons, name="coupons"),
    path(
        "purchase-complete/<str:order>/",
        views.purchase_complete,
        name="purchase-complete",
    ),
    # Ticket assignment
    path(
        "create/<str:order>/",
        views.CreateTicketView.as_view(),
        name="create_ticket",
    ),
    path(
        "detail/<str:order>/",
        views.TicketDetailView.as_view(),
        name="detail",
    ),
    path(
        "sales/<int:pk>/",
        views.SalesTicketView.as_view(),
        name="sales",
    ),
    # Paystack integration
    path(
        "paystack/validate/<str:order>/<str:code>/",
        views.validate_paystack_ref,
        name="validate_paystack",
    ),
    path(
        "paystack/webhook/",
        csrf_exempt(views.paystack_webhook),
        name="paystack_webhook",
    ),
    path(
        "paystack/callback/<str:order>/",
        csrf_exempt(views.PaystackCallbackView.as_view()),
        name="paystack_callback",
    ),
]
