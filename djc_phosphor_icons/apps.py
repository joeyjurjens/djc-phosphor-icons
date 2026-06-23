from django.apps import AppConfig


class PhosphorIconsConfig(AppConfig):
    name = "djc_phosphor_icons"

    def ready(self) -> None:
        from djc_phosphor_icons.app_settings import get_setting
        from djc_phosphor_icons.components.icon import Icon

        if get_setting("auto_register", True):
            from django_components import register

            register(get_setting("component_name", "Icon"))(Icon)
