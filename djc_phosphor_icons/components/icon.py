from typing import Any, NamedTuple

from django.template import Context
from django_components import Component, Default, merge_attributes, types
from django_components.extensions.cache import ComponentCache

from djc_phosphor_icons.app_settings import get_setting
from djc_phosphor_icons.svgs import get_svg_inner, validate


class Icon(Component):
    class Cache(ComponentCache):
        @property
        def enabled(self) -> bool:
            return get_setting("cache", True)

    class Kwargs(NamedTuple):
        name: str
        weight: str
        style: str
        size: str | int | None
        color: str | None
        mirrored: bool
        attrs: dict[str, Any] | None

    class Defaults:
        weight = Default(lambda: get_setting("default_weight", "regular"))
        style = Default(lambda: get_setting("default_style", "flat"))
        size = None
        color = None
        mirrored = False
        attrs = None

    def get_attrs(self, kwargs: "Icon.Kwargs") -> dict[str, Any]:
        """Attributes the component sets itself. Merged over the caller's `attrs`,
        so `class` and `style` are appended to it rather than replaced by it."""
        style = []
        if kwargs.size:
            size = f"{kwargs.size}px" if isinstance(kwargs.size, int) else kwargs.size
            style.append(f"width: {size}; height: {size};")
        if kwargs.color:
            style.append(f"color: {kwargs.color};")
        if kwargs.mirrored:
            style.append("transform: scaleX(-1);")

        return {"style": " ".join(style)} if style else {}

    def get_default_attrs(self, kwargs: "Icon.Kwargs") -> dict[str, Any]:
        """Attributes the caller's `attrs` may override."""
        attrs = {
            "xmlns": "http://www.w3.org/2000/svg",
            "viewBox": "0 0 256 256",
            "aria-hidden": "true",
        }
        if kwargs.style == "flat" or kwargs.weight == "fill":
            attrs["fill"] = "currentColor"
        return attrs

    def get_template_data(self, args, kwargs: "Icon.Kwargs", slots, context: Context) -> dict:
        validate(kwargs.weight, kwargs.style)
        return {
            "svg_inner": get_svg_inner(kwargs.name, kwargs.weight, kwargs.style),
            "attrs": merge_attributes(kwargs.attrs or {}, self.get_attrs(kwargs)),
            "default_attrs": self.get_default_attrs(kwargs),
        }

    template: types.django_html = """
        {% load component_tags %}
        <svg {% html_attrs attrs default_attrs %}>
            {% slot "title" default %}{% endslot %}{{ svg_inner|safe }}
        </svg>
    """
