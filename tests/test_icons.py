from unittest.mock import patch

import pytest
from django.test import override_settings

from djc_phosphor_icons.components.icon import Icon
from djc_phosphor_icons.svgs import VALID_STYLES, VALID_WEIGHTS, exists, icon_names


def all_icon_combinations():
    return [
        (name, weight, style)
        for name in icon_names()
        for weight in sorted(VALID_WEIGHTS)
        for style in sorted(VALID_STYLES)
    ]


def shipped_combinations():
    return [combo for combo in all_icon_combinations() if exists(*combo)]


def unshipped_combinations():
    """Combinations Phosphor itself is missing - see "Known Icon Issues" in the README."""
    return [combo for combo in all_icon_combinations() if not exists(*combo)]


@pytest.mark.parametrize("name,weight,style", shipped_combinations())
def test_icon_renders(name, weight, style):
    output = Icon.render(kwargs={"name": name, "weight": weight, "style": style})
    assert "<svg" in output


@pytest.mark.parametrize("name,weight,style", unshipped_combinations())
def test_unshipped_icon_raises_with_suggestions(name, weight, style):
    with pytest.raises(FileNotFoundError) as excinfo:
        Icon.render(kwargs={"name": name, "weight": weight, "style": style})
    assert name in str(excinfo.value)


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
