import difflib
import re
from pathlib import Path
from typing import Any

from django.template import Context
from django_components import Component, Default, types
from django_components.extensions.cache import ComponentCache

from djc_phosphor_icons.app_settings import get_setting

SVGS_DIR = Path(__file__).parent.parent / "svgs"

VALID_WEIGHTS = frozenset({"bold", "duotone", "fill", "light", "regular", "thin"})
VALID_STYLES = frozenset({"flat", "stroke"})

SVG_INNER_RE = re.compile(r"<svg[^>]*>(.*)</svg>", re.DOTALL)


class Icon(Component):
    class Cache(ComponentCache):
        @property
        def enabled(self) -> bool:
            return get_setting("cache", True)

    class Kwargs:
        name: str
        weight: str
        style: str
        size: int | None
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

    def get_template_data(self, args, kwargs: "Icon.Kwargs", slots, context: Context) -> dict:
        if kwargs.weight not in VALID_WEIGHTS:
            raise ValueError(
                f"Invalid weight '{kwargs.weight}'. Choose from: {', '.join(sorted(VALID_WEIGHTS))}"
            )
        if kwargs.style not in VALID_STYLES:
            raise ValueError(
                f"Invalid style '{kwargs.style}'. Choose from: {', '.join(sorted(VALID_STYLES))}"
            )

        filename = kwargs.name if kwargs.weight == "regular" else f"{kwargs.name}-{kwargs.weight}"
        svg_path = SVGS_DIR / kwargs.style / kwargs.weight / f"{filename}.svg"

        if not svg_path.exists():
            icon_names = [
                p.stem
                for p in (SVGS_DIR / kwargs.style / "regular").iterdir()
                if p.suffix == ".svg"
            ]
            fuzzy = difflib.get_close_matches(kwargs.name, icon_names, n=3, cutoff=0.6)
            hint = f" Did you mean: {', '.join(fuzzy)}?" if fuzzy else ""
            raise FileNotFoundError(
                f"Icon '{kwargs.name}' "
                f"(weight: {kwargs.weight}, style: {kwargs.style}) not found.{hint}"
            )

        match = SVG_INNER_RE.search(svg_path.read_text())
        svg_inner = match.group(1) if match else ""

        style_parts = []
        if kwargs.size is not None:
            style_parts.append(f"width: {kwargs.size}px; height: {kwargs.size}px;")
        if kwargs.color is not None:
            style_parts.append(f"color: {kwargs.color};")
        if kwargs.mirrored:
            style_parts.append("transform: scaleX(-1);")

        default_attrs: dict[str, Any] = {
            "xmlns": "http://www.w3.org/2000/svg",
            "viewBox": "0 0 256 256",
            "aria-hidden": "true",
        }
        if kwargs.style == "flat":
            default_attrs["fill"] = "currentColor"
        if style_parts:
            default_attrs["style"] = " ".join(style_parts)

        return {
            "svg_inner": svg_inner,
            "default_attrs": default_attrs,
            "attrs": kwargs.attrs,
        }

    template: types.django_html = """
        {% load component_tags %}
        <svg {% html_attrs attrs default_attrs %}>
            {% slot "title" default %}{% endslot %}{{ svg_inner|safe }}
        </svg>
    """
