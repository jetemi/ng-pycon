from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class FeatureBlock(blocks.StructBlock):
    """A feature card block with icon, title, and description."""
    icon_svg = blocks.TextBlock(
        required=False,
        help_text="SVG code for the icon (optional)"
    )
    title = blocks.CharBlock(max_length=100)
    description = blocks.TextBlock()
    link_text = blocks.CharBlock(max_length=50, required=False)
    link_url = blocks.URLBlock(required=False)
    
    class Meta:
        icon = "doc-full"
        label = "Feature Card"


class HomePage(Page):
    # Hero Section
    hero_title = models.CharField(
        max_length=200, 
        default="PyCon Nigeria",
        help_text="Main hero title"
    )
    hero_subtitle = models.CharField(
        max_length=200,
        blank=True,
        help_text="Subtitle text (optional)"
    )
    hero_description = RichTextField(
        blank=True,
        help_text="Hero section description"
    )
    hero_primary_button_text = models.CharField(
        max_length=50,
        default="Register Now",
        help_text="Primary call-to-action button text"
    )
    hero_primary_button_url = models.URLField(blank=True)
    hero_secondary_button_text = models.CharField(
        max_length=50,
        default="Call for Papers",
        help_text="Secondary button text"
    )
    hero_secondary_button_url = models.URLField(blank=True)
    
    # Conference Info Section
    conference_section_title = models.CharField(
        max_length=200,
        default="Conference Highlights",
        help_text="Title for the main conference section"
    )
    conference_description = RichTextField(
        blank=True,
        help_text="Description of the conference"
    )
    
    # Features
    features = StreamField([
        ('feature', FeatureBlock()),
    ], blank=True, help_text="Add feature cards to showcase conference highlights")
    
    # Year Navigation Section
    year_navigation_title = models.CharField(
        max_length=200,
        default="Browse Conference Years",
        help_text="Title for the year navigation section"
    )
    year_navigation_description = RichTextField(
        blank=True,
        help_text="Description for the year navigation section"
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_description'),
            FieldPanel('hero_primary_button_text'),
            FieldPanel('hero_primary_button_url'),
            FieldPanel('hero_secondary_button_text'),
            FieldPanel('hero_secondary_button_url'),
        ], heading="Hero Section"),
        
        MultiFieldPanel([
            FieldPanel('conference_section_title'),
            FieldPanel('conference_description'),
        ], heading="Conference Info"),
        
        FieldPanel('features'),
        
        MultiFieldPanel([
            FieldPanel('year_navigation_title'),
            FieldPanel('year_navigation_description'),
        ], heading="Year Navigation"),
    ]

    class Meta:
        verbose_name = "Home Page"
