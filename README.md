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
{% component "Icon" name="house" weight="bold" / %}
{% component "Icon" name="house" style="stroke" size=24 color="#ff0000" / %}
```

| Kwarg | Type | Default | Description |
|---|---|---|---|
| `name` | `str` | — | Icon name, e.g. `"house"` |
| `weight` | `str` | `"regular"` | `bold`, `duotone`, `fill`, `light`, `regular`, `thin` |
| `style` | `str` | `"flat"` | `flat` or `stroke` |
| `size` | `str` or `int` | `None` | Sets width and height; any CSS length (`"1.5rem"`), an `int` is read as px |
| `color` | `str` | `None` | Sets CSS `color` |
| `mirrored` | `bool` | `False` | Flips the icon horizontally |
| `attrs` | `dict` | `None` | Extra attributes passed to the `<svg>` element |

`class` and `style` from `attrs` are combined with the component's own, not replaced by them - so passing `attrs={"class": "me-2"}` keeps whatever the component already sets, and `size` still wins over a conflicting `width` in your `style`.

## Subclassing

`Kwargs` and `Defaults` are inherited, so a subclass only declares what it changes. `get_attrs()` returns what the component sets on the `<svg>` itself, `get_default_attrs()` what the caller's `attrs` may override - extend either to add your own class, `aria-label` or `data-` attribute:

```python
from django_components import merge_attributes
from djc_phosphor_icons import Icon


class MyIcon(Icon):
    def get_attrs(self, kwargs):
        return merge_attributes({"class": "icon"}, super().get_attrs(kwargs))
```

## Search and metadata

Every icon ships with the tags, categories and aliases that power search on [phosphoricons.com](https://phosphoricons.com), so you can build an icon picker without calling out to an API. `search_icons()` mirrors that site's ranking: names weigh four times heavier than tags and categories, and near-misses still match.

```python
from djc_phosphor_icons.search import search_icons

search_icons("arrow left")               # ranked, best match first
search_icons("roledex")                  # matches on tags: address-book
search_icons("cart", categories="Commerce")
search_icons()                           # every icon, alphabetically
```

```python
from djc_phosphor_icons.search import all_icons, categories, get_icon

get_icon("house").tags                   # ('homes', 'buildings', 'places', 'locations')
get_icon("caduceus").name                # 'asclepius' - aliases resolve
categories()                             # ('Arrows', 'Brand', ... ) - for filter dropdowns
len(all_icons())
```

The same search answers a wrong `name`, so the error suggests by tag as well as by spelling - `{% component "Icon" name="cart" / %}` raises `Did you mean: shopping-cart, shopping-cart-simple, car?`, narrowed to icons that exist in the requested weight and style.

To retune the ranking, subclass `Ranking` and point `PHOSPHOR_ICONS["ranking"]` at it. Override the weights and thresholds, or `score()` for a different algorithm entirely:

```python
from djc_phosphor_icons.search import Ranking


class MyRanking(Ranking):
    name_weight = 8.0
    fuzzy_cutoff = 0.9
```

A one-off ranking can also be passed straight in: `search_icons("cart", ranking=MyRanking())`.

The raw SVGs are reachable too, for when you need the markup outside a template:

```python
from djc_phosphor_icons.svgs import get_svg, get_svg_inner, icon_names

get_svg("house", weight="bold", style="flat")
get_svg_inner("house")                   # without the wrapping <svg> tag
icon_names()
```

## Settings

Configure via `PHOSPHOR_ICONS` in your Django settings:

```python
PHOSPHOR_ICONS = {
    "auto_register": True,        # Auto-register the component on startup (default: True)
    "component_name": "Icon",     # Template tag name (default: "Icon")
    "default_style": "flat",      # Default style (default: "flat")
    "default_weight": "regular",   # Default weight (default: "regular")
    "cache": True,                # Cache rendered output per unique set of kwargs (default: True)
    "ranking": "myapp.MyRanking", # Dotted path to a Ranking subclass (default: the bundled one)
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

To refresh the metadata (tags, categories, aliases) from the Phosphor API:

```bash
uv run python scripts/download_metadata.py
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
