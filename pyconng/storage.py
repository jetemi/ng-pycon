import logging

from django.contrib.staticfiles.storage import ManifestStaticFilesStorage

logger = logging.getLogger(__name__)


class ForgivingManifestStaticFilesStorage(ManifestStaticFilesStorage):
    """Returns unhashed URL for missing manifest entries instead of crashing."""
    manifest_strict = False

    def hashed_name(self, name, content=None, filename=None):
        try:
            return super().hashed_name(name, content, filename)
        except ValueError:
            logger.warning("Static file not found, using unhashed: %s", name)
            return name
