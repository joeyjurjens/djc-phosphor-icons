from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

SECRET_KEY = "test-secret-key"

INSTALLED_APPS = [
    "django_components",
    "djc_phosphor_icons",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [],
            "builtins": ["django_components.templatetags.component_tags"],
            "loaders": ["django.template.loaders.app_directories.Loader"],
        },
    }
]

ROOT_URLCONF = "tests.urls"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
