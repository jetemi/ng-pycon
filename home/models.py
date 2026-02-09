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


class NavigationMenuItemBlock(blocks.StructBlock):
    """A navigation menu item."""
    label = blocks.CharBlock(max_length=50, required=True)
    link_url = blocks.CharBlock(max_length=200, required=True, help_text="URL or page path (e.g., /tickets/ or https://example.com)")
    
    class Meta:
        icon = "link"
        label = "Menu Item"


class TicketBlock(blocks.StructBlock):
    """A ticket pricing tier."""
    tier_name = blocks.CharBlock(max_length=100, required=True, help_text="e.g., Student, Personal, Business")
    price = blocks.CharBlock(max_length=50, required=True, help_text="e.g., €60, $200, Free")
    description = blocks.TextBlock(required=True)
    button_text = blocks.CharBlock(max_length=50, default="Buy Tickets")
    button_url = blocks.URLBlock(required=False)
    
    class Meta:
        icon = "ticket"
        label = "Ticket Tier"


class SponsorBlock(blocks.StructBlock):
    """A sponsor entry."""
    name = blocks.CharBlock(max_length=200, required=True)
    logo = ImageChooserBlock(required=True)
    tier = blocks.ChoiceBlock(
        choices=[
            ('gold', 'Gold'),
            ('silver', 'Silver'),
            ('bronze', 'Bronze'),
            ('patron', 'Patron'),
            ('startup', 'Startup'),
            ('media', 'Media Partner'),
        ],
        required=True
    )
    website_url = blocks.URLBlock(required=False)
    
    class Meta:
        icon = "image"
        label = "Sponsor"


class FooterLinkBlock(blocks.StructBlock):
    """A footer link."""
    label = blocks.CharBlock(max_length=100, required=True)
    url = blocks.CharBlock(max_length=200, required=True)
    
    class Meta:
        icon = "link"
        label = "Footer Link"


class HomePage(Page):
    """
    Home page for PyCon Nigeria conference.
    Can be used for both current year (at root /) and archived years (at /2024/, /2025/, etc.)
    Each instance can have its own theme/design.
    """
    
    # Conference Year & Theme
    conference_year = models.IntegerField(
        null=True,
        blank=True,
        help_text="The conference year this page represents (e.g., 2024, 2025). Leave blank for current year."
    )
    
    # Theme/Design selection
    THEME_CHOICES = [
        ('default', 'Default Theme (current design)'),
        ('theme_2024', '2024 Theme'),
        ('theme_2025', '2025 Theme'),
        ('theme_2026', '2026 Theme'),
        ('theme_legacy', 'Legacy Theme'),
    ]
    
    theme = models.CharField(
        max_length=50,
        choices=THEME_CHOICES,
        default='default',
        help_text="Select the design/theme for this conference year"
    )
    
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
    
    # Conference Location & Dates
    conference_location = models.CharField(
        max_length=200,
        blank=True,
        help_text="Conference location (e.g., Lagos, Nigeria)"
    )
    conference_dates = models.CharField(
        max_length=200,
        blank=True,
        help_text="Conference dates (e.g., May 15-17, 2025)"
    )
    
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
    
    # Navigation Menu
    navigation_menu_items = StreamField([
        ('menu_item', NavigationMenuItemBlock()),
    ], blank=True, help_text="Navigation menu items")
    login_button_text = models.CharField(
        max_length=50,
        default="Login",
        blank=True,
        help_text="Login button text (leave blank to hide)"
    )
    login_button_url = models.URLField(
        blank=True,
        help_text="Login button URL"
    )
    
    # Ticket Pricing Section
    ticket_section_title = models.CharField(
        max_length=200,
        default="Tickets",
        blank=True,
        help_text="Ticket pricing section title"
    )
    ticket_pricing = StreamField([
        ('ticket', TicketBlock()),
    ], blank=True, help_text="Add ticket pricing tiers")
    
    # Sponsor Section
    sponsor_section_title = models.CharField(
        max_length=200,
        default="Sponsors",
        blank=True,
        help_text="Sponsor section title"
    )
    sponsors = StreamField([
        ('sponsor', SponsorBlock()),
    ], blank=True, help_text="Add sponsors")
    
    # Community Voting Section
    voting_section_title = models.CharField(
        max_length=200,
        default="Community Voting",
        blank=True,
        help_text="Voting section title"
    )
    voting_deadline = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Voting deadline (for countdown timer)"
    )
    voting_description = RichTextField(
        blank=True,
        help_text="Voting section description"
    )
    voting_button_text = models.CharField(
        max_length=50,
        default="Vote Now",
        blank=True,
        help_text="Voting button text"
    )
    voting_button_url = models.URLField(
        blank=True,
        help_text="Voting button URL"
    )
    
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
    
    # Footer
    footer_copyright = models.CharField(
        max_length=200,
        default="© PyCon Nigeria. All rights reserved.",
        blank=True,
        help_text="Footer copyright text"
    )
    footer_links = StreamField([
        ('link', FooterLinkBlock()),
    ], blank=True, help_text="Footer links (Privacy Policy, FAQs, etc.)")
    
    # Social Media
    twitter_url = models.URLField(blank=True, help_text="Twitter/X URL")
    facebook_url = models.URLField(blank=True, help_text="Facebook URL")
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn URL")
    instagram_url = models.URLField(blank=True, help_text="Instagram URL")
    youtube_url = models.URLField(blank=True, help_text="YouTube URL")
    github_url = models.URLField(blank=True, help_text="GitHub URL")
    
    # Newsletter
    newsletter_title = models.CharField(
        max_length=200,
        default="Stay tuned!",
        blank=True,
        help_text="Newsletter section title"
    )
    newsletter_description = models.CharField(
        max_length=500,
        blank=True,
        help_text="Newsletter description"
    )

    # Allow HomePage to be nested (for archived years) and have standard pages as children
    parent_page_types = ["wagtailcore.Page", "home.HomePage"]  # Can be root or child of another HomePage
    subpage_types = ["home.StandardPage", "home.HomePage"]  # Can have standard pages and other year homepages

    def get_default_child_class(self):
        from .models import StandardPage
        return StandardPage
    
    def get_template(self, request, *args, **kwargs):
        """
        Dynamically select template based on the chosen theme.
        This allows different conference years to have completely different designs.
        """
        theme_templates = {
            'default': 'home/home_page.html',
            'theme_2024': 'home/themes/theme_2024.html',
            'theme_2025': 'home/themes/theme_2025.html',
            'theme_2026': 'home/themes/theme_2026.html',
            'theme_legacy': 'home/themes/theme_legacy.html',
        }
        return theme_templates.get(self.theme, 'home/home_page.html')
    
    def save(self, *args, **kwargs):
        """Auto-set slug and title based on conference year if specified."""
        if self.conference_year:
            # For archived years, set slug to the year
            if not self.slug or self.slug == 'home':
                self.slug = str(self.conference_year)
            # Auto-set title if not customized
            if not self.title or self.title == "Home":
                self.title = f"PyCon Nigeria {self.conference_year}"
        return super().save(*args, **kwargs)
    
    def get_context(self, request, *args, **kwargs):
        """
        Add theme information to context for this HomePage.
        """
        context = super().get_context(request, *args, **kwargs)
        context['page_theme'] = self.theme
        context['page_conference_year'] = self.conference_year
        return context

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('conference_year'),
            FieldPanel('theme'),
        ], heading="Conference Year & Theme"),
        
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_description'),
            FieldPanel('conference_location'),
            FieldPanel('conference_dates'),
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
            FieldPanel('ticket_section_title'),
            FieldPanel('ticket_pricing'),
        ], heading="Ticket Pricing"),
        
        MultiFieldPanel([
            FieldPanel('sponsor_section_title'),
            FieldPanel('sponsors'),
        ], heading="Sponsors"),
        
        MultiFieldPanel([
            FieldPanel('voting_section_title'),
            FieldPanel('voting_deadline'),
            FieldPanel('voting_description'),
            FieldPanel('voting_button_text'),
            FieldPanel('voting_button_url'),
        ], heading="Community Voting"),
        
        MultiFieldPanel([
            FieldPanel('navigation_menu_items'),
            FieldPanel('login_button_text'),
            FieldPanel('login_button_url'),
        ], heading="Navigation"),
        
        MultiFieldPanel([
            FieldPanel('year_navigation_title'),
            FieldPanel('year_navigation_description'),
        ], heading="Year Navigation"),
        
        MultiFieldPanel([
            FieldPanel('footer_copyright'),
            FieldPanel('footer_links'),
            FieldPanel('newsletter_title'),
            FieldPanel('newsletter_description'),
        ], heading="Footer"),
        
        MultiFieldPanel([
            FieldPanel('twitter_url'),
            FieldPanel('facebook_url'),
            FieldPanel('linkedin_url'),
            FieldPanel('instagram_url'),
            FieldPanel('youtube_url'),
            FieldPanel('github_url'),
        ], heading="Social Media"),
    ]

    class Meta:
        verbose_name = "Home Page"


class NewsletterSubscriber(models.Model):
    """Newsletter subscriber model."""
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email


class StandardPage(Page):
    """A generic, reusable content page for most site pages."""
    intro = RichTextField(blank=True)
    body = StreamField([
        ("heading", blocks.CharBlock(form_classname="full title")),
        ("paragraph", blocks.RichTextBlock()),
        ("image", ImageChooserBlock()),
    ], blank=True, use_json_field=True)

    parent_page_types = ["home.HomePage", "home.StandardPage"]
    subpage_types = ["home.StandardPage"]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
    ]
    
    def get_parent_homepage(self):
        """
        Traverse up the page tree to find the parent HomePage.
        This allows child pages to inherit theme from their year's homepage.
        """
        parent = self.get_parent()
        
        while parent:
            if isinstance(parent.specific, HomePage):
                return parent.specific
            parent = parent.get_parent()
        
        return None
    
    def get_context(self, request, *args, **kwargs):
        """
        Add parent HomePage theme information to context.
        This allows child pages to use the same theme as their parent year.
        """
        context = super().get_context(request, *args, **kwargs)
        
        # Get parent HomePage to inherit theme
        parent_homepage = self.get_parent_homepage()
        
        if parent_homepage:
            context['parent_homepage'] = parent_homepage
            context['page_theme'] = parent_homepage.theme
            context['page_conference_year'] = parent_homepage.conference_year
        else:
            context['page_theme'] = 'default'
            context['page_conference_year'] = None
        
        return context

    class Meta:
        verbose_name = "Standard Page"


