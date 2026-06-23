from unittest.mock import patch

import pytest
from django.test import override_settings

from djc_phosphor_icons.components.icon import SVGS_DIR, VALID_STYLES, VALID_WEIGHTS, Icon


def all_icon_combinations():
    names = sorted(p.stem for p in (SVGS_DIR / "flat" / "regular").glob("*.svg"))
    return [
        (name, weight, style)
        for name in names
        for weight in sorted(VALID_WEIGHTS)
        for style in sorted(VALID_STYLES)
    ]


@pytest.mark.parametrize("name,weight,style", all_icon_combinations())
def test_icon_renders(name, weight, style):
    output = Icon.render(kwargs={"name": name, "weight": weight, "style": style})
    assert "<svg" in output


@override_settings(PHOSPHOR_ICONS={"cache": True})
def test_cache_hits_on_second_render():
    with patch.object(
        Icon, "get_template_data", autospec=True, wraps=Icon.get_template_data
    ) as mock:
        Icon.render(kwargs={"name": "house", "weight": "regular", "style": "flat"})
        Icon.render(kwargs={"name": "house", "weight": "regular", "style": "flat"})
        assert mock.call_count == 1


@override_settings(PHOSPHOR_ICONS={"cache": False})
def test_cache_disabled_renders_twice():
    with patch.object(
        Icon, "get_template_data", autospec=True, wraps=Icon.get_template_data
    ) as mock:
        Icon.render(kwargs={"name": "house", "weight": "regular", "style": "flat"})
        Icon.render(kwargs={"name": "house", "weight": "regular", "style": "flat"})
        assert mock.call_count == 2
