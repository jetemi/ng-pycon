"""
Travel Grant application form.
"""

from decimal import Decimal

from django import forms

from .models import TravelGrantApplication, TravelGrantPayment, EMPLOYMENT_CHOICES

TAILWIND_INPUT = (
    "w-full px-4 py-2 border border-gray-300 rounded-lg "
    "focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
)
TAILWIND_SELECT = (
    "w-full px-4 py-2 border border-gray-300 rounded-lg bg-white "
    "focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
)
TAILWIND_TEXTAREA = (
    "w-full px-4 py-2 border border-gray-300 rounded-lg "
    "focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent "
    "resize-y"
)
TAILWIND_CHECKBOX = (
    "w-4 h-4 text-teal-600 border-gray-300 rounded focus:ring-teal-500"
)
TAILWIND_NUMBER = TAILWIND_INPUT


class TravelGrantApplicationForm(forms.ModelForm):
    """Full application form for Sections A-F."""

    class Meta:
        model = TravelGrantApplication
        fields = [
            "country_of_residence",
            "city",
            "passport_required",
            "first_time_pycon",
            "community_involvement",
            "financial_need_reason",
            "employment_status",
            "is_student",
            "estimated_transport_cost",
            "estimated_accommodation_cost",
            "other_funding_sources",
            "other_funding_details",
            "community_impact",
            "commit_to_share_learnings",
            "confirm_accurate",
            "agree_to_refund",
        ]
        widgets = {
            "country_of_residence": forms.TextInput(attrs={
                "class": TAILWIND_INPUT,
                "placeholder": "e.g. Nigeria",
            }),
            "city": forms.TextInput(attrs={
                "class": TAILWIND_INPUT,
                "placeholder": "e.g. Lagos",
            }),
            "passport_required": forms.CheckboxInput(attrs={"class": TAILWIND_CHECKBOX}),
            "first_time_pycon": forms.CheckboxInput(attrs={"class": TAILWIND_CHECKBOX}),
            "community_involvement": forms.Textarea(attrs={
                "class": TAILWIND_TEXTAREA,
                "rows": 4,
                "placeholder": "Describe your involvement in the Python community...",
            }),
            "financial_need_reason": forms.Textarea(attrs={
                "class": TAILWIND_TEXTAREA,
                "rows": 5,
                "placeholder": "Why do you need financial assistance to attend?",
            }),
            "employment_status": forms.Select(
                choices=EMPLOYMENT_CHOICES,
                attrs={"class": TAILWIND_SELECT},
            ),
            "is_student": forms.CheckboxInput(attrs={"class": TAILWIND_CHECKBOX}),
            "estimated_transport_cost": forms.NumberInput(attrs={
                "class": TAILWIND_NUMBER,
                "min": "0",
                "step": "0.01",
                "placeholder": "0.00",
            }),
            "estimated_accommodation_cost": forms.NumberInput(attrs={
                "class": TAILWIND_NUMBER,
                "min": "0",
                "step": "0.01",
                "placeholder": "0.00",
            }),
            "other_funding_sources": forms.CheckboxInput(attrs={"class": TAILWIND_CHECKBOX}),
            "other_funding_details": forms.Textarea(attrs={
                "class": TAILWIND_TEXTAREA,
                "rows": 3,
                "placeholder": "Details of other funding (optional)",
            }),
            "community_impact": forms.Textarea(attrs={
                "class": TAILWIND_TEXTAREA,
                "rows": 5,
                "placeholder": "How will attending PyCon benefit your community?",
            }),
            "commit_to_share_learnings": forms.CheckboxInput(attrs={"class": TAILWIND_CHECKBOX}),
            "confirm_accurate": forms.CheckboxInput(attrs={"class": TAILWIND_CHECKBOX}),
            "agree_to_refund": forms.CheckboxInput(attrs={"class": TAILWIND_CHECKBOX}),
        }

    def __init__(self, *args, submit_action=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.submit_action = submit_action

    def clean(self):
        data = super().clean()
        if self.submit_action:
            if not data.get("confirm_accurate"):
                self.add_error("confirm_accurate", "You must confirm the information is accurate.")
            if not data.get("agree_to_refund"):
                self.add_error("agree_to_refund", "You must agree to refund if information is misrepresented.")
        return data

class GrantReviewForm(forms.Form):
    """Review scores and comments."""

    need_score = forms.IntegerField(
        min_value=1, max_value=5,
        widget=forms.NumberInput(attrs={
            "class": TAILWIND_INPUT, "min": "1", "max": "5",
        }),
    )
    impact_score = forms.IntegerField(
        min_value=1, max_value=5,
        widget=forms.NumberInput(attrs={
            "class": TAILWIND_INPUT, "min": "1", "max": "5",
        }),
    )
    contribution_score = forms.IntegerField(
        min_value=1, max_value=5,
        widget=forms.NumberInput(attrs={
            "class": TAILWIND_INPUT, "min": "1", "max": "5",
        }),
    )
    diversity_score = forms.IntegerField(
        min_value=1, max_value=5,
        widget=forms.NumberInput(attrs={
            "class": TAILWIND_INPUT, "min": "1", "max": "5",
        }),
    )
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": TAILWIND_TEXTAREA, "rows": 4,
        }),
    )

class GrantAssignReviewerForm(forms.Form):
    application_ids = forms.CharField(widget=forms.HiddenInput())
    reviewer_ids = forms.CharField(widget=forms.HiddenInput())

    def clean_application_ids(self):
        raw = self.cleaned_data["application_ids"]
        return [x.strip() for x in raw.split(",") if x.strip()]

    def clean_reviewer_ids(self):
        raw = self.cleaned_data["reviewer_ids"]
        return [int(x.strip()) for x in raw.split(",") if x.strip()]


class GrantBulkDecisionForm(forms.Form):
    DECISION_CHOICES = [
        ("approve", "Approve"),
        ("reject", "Reject"),
        ("waitlist", "Waitlist"),
    ]
    application_ids = forms.CharField(widget=forms.HiddenInput())
    decision = forms.ChoiceField(choices=DECISION_CHOICES, widget=forms.Select(attrs={"class": TAILWIND_SELECT}))

    def clean_application_ids(self):
        raw = self.cleaned_data["application_ids"]
        return [x.strip() for x in raw.split(",") if x.strip()]


class GrantPaymentForm(forms.Form):
    """Finance: mark payment status."""
    payment_status = forms.ChoiceField(
        choices=TravelGrantPayment.STATUS_CHOICES,
        widget=forms.Select(attrs={"class": TAILWIND_SELECT}),
    )
    amount_paid = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={"class": TAILWIND_INPUT, "step": "0.01"}),
    )
    reference = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": TAILWIND_INPUT, "placeholder": "Transaction reference"}),
    )
    receipt = forms.FileField(required=False)
