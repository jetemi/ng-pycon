from django.contrib.staticfiles.storage import ManifestStaticFilesStorage


class ForgivingManifestStaticFilesStorage(ManifestStaticFilesStorage):
    """Returns unhashed URL for missing manifest entries instead of crashing."""
    manifest_strict = False
