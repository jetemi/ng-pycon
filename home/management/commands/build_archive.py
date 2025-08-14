import os
from urllib.parse import urljoin

from django.conf import settings
from django.core.management.base import BaseCommand
from django.test import Client
from wagtail.models import Page, Site

ARCHIVE_DIR = os.path.join(settings.BASE_DIR, 'archives')


class Command(BaseCommand):
    help = "Build static HTML archive for a given year into archives/<year>"

    def add_arguments(self, parser):
        parser.add_argument('year', type=int, help='Conference year to archive, e.g., 2024')

    def handle(self, *args, **options):
        year = options['year']
        os.makedirs(os.path.join(ARCHIVE_DIR, str(year)), exist_ok=True)

        client = Client()

        # Determine site and starting URLs
        site = Site.objects.get(is_default_site=True)
        root = site.root_page.specific

        # Collect URLs to snapshot: home and all live pages under home
        urls = set()

        # Home
        urls.add('/')

        # Add child pages under the first HomePage child if exists, otherwise all live pages
        try:
            from home.models import HomePage
            home = root.get_children().type(HomePage).live().first()
        except Exception:
            home = None

        if home:
            for p in Page.objects.descendant_of(home).live().public():
                url = p.get_url(request=None) or '/'
                if url:
                    urls.add(url)
        else:
            for p in Page.objects.live().public():
                url = p.get_url(request=None) or '/'
                if url:
                    urls.add(url)

        # Always include some common routes
        urls.update({'/search/'})

        self.stdout.write(self.style.NOTICE(f"Building archive for {year} with {len(urls)} urls"))

        # Fetch each URL under the year namespace (so context processors set that theme)
        num_ok = 0
        for url in sorted(urls):
            year_url = f"/{year}{url}"
            response = client.get(year_url, follow=True)
            if response.status_code == 200:
                # Map URL to file path
                rel_path = url.strip('/') or 'index'
                out_path = os.path.join(ARCHIVE_DIR, str(year), f"{rel_path}.html")
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                with open(out_path, 'wb') as f:
                    f.write(response.content)
                num_ok += 1
                self.stdout.write(self.style.SUCCESS(f"✔ {year_url} -> {out_path}"))
            else:
                self.stdout.write(self.style.WARNING(f"✖ {year_url} ({response.status_code})"))

        self.stdout.write(self.style.SUCCESS(f"Done. {num_ok}/{len(urls)} pages archived to {ARCHIVE_DIR}/{year}")) 