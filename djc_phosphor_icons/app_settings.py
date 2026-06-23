from django.conf import settings


def get_setting(key: str, default):
    return getattr(settings, "PHOSPHOR_ICONS", {}).get(key, default)
