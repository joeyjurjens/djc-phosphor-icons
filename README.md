# djc-phosphor-icons

[Phosphor Icons](https://phosphoricons.com) as [django-components](https://github.com/EmilStenstrom/django-components).

[Browse all icons →](https://joeyjurjens.github.io/djc-phosphor-icons/preview.html)

## Installation

```bash
pip install djc-phosphor-icons
```

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    "django_components",
    "djc_phosphor_icons",
]
```

## Usage

```html
{% component "Icon" name="house" / %}
{% component "Icon" name="house" variant="bold" / %}
{% component "Icon" name="house" style="stroke" size=24 color="#ff0000" / %}
```

| Kwarg | Type | Default | Description |
|---|---|---|---|
| `name` | `str` | — | Icon name, e.g. `"house"` |
| `variant` | `str` | `"regular"` | `bold`, `duotone`, `fill`, `light`, `regular`, `thin` |
| `style` | `str` | `"flat"` | `flat` or `stroke` |
| `size` | `int` | `None` | Sets width and height in px |
| `color` | `str` | `None` | Sets CSS `color` |
| `mirrored` | `bool` | `False` | Flips the icon horizontally |
| `attrs` | `dict` | `None` | Extra attributes passed to the `<svg>` element |

## Settings

Configure via `PHOSPHOR_ICONS` in your Django settings:

```python
PHOSPHOR_ICONS = {
    "auto_register": True,        # Auto-register the component on startup (default: True)
    "component_name": "Icon",     # Template tag name (default: "Icon")
    "default_style": "flat",      # Default style (default: "flat")
    "default_variant": "regular", # Default variant (default: "regular")
    "cache": True,                # Cache rendered output per unique set of kwargs (default: True)
}
```

## Development

```bash
uv sync
uv run pytest
uv run ruff check .
uv run ruff format .
```

To update the icon set to a specific Phosphor release (for local inspection only — the `update-icons` GitHub Action handles this automatically when committing):

```bash
uv run python scripts/download_icons.py v2.1.0
```

To generate a visual preview of all icons:

```bash
uv run python scripts/preview_icons.py
```

<!-- known-issues-start -->
## Known Icon Issues

The following icons are incomplete in the upstream Phosphor release and will fail to render in certain combinations:

- **book-user**: missing from `stroke/light`, `stroke/bold`, `stroke/fill`, `stroke/duotone`
<!-- known-issues-end -->
