from difflib import SequenceMatcher
from functools import cache

from django.utils.module_loading import import_string

from djc_phosphor_icons.app_settings import get_setting
from djc_phosphor_icons.search.metadata import IconEntry


class Ranking:
    """Mirrors the Fuse.js configuration phosphoricons.com searches with: `name`
    weighs four times heavier than tags, categories and codepoint, and
    near-misses still match. Subclass to retune or to replace `score()`
    outright, then point `PHOSPHOR_ICONS["ranking"]` at it."""

    name_weight = 4.0
    field_weight = 1.0

    exact_score = 1.0
    prefix_score = 0.9
    substring_score = 0.7
    fuzzy_score = 0.5
    fuzzy_cutoff = 0.8

    def match(self, token: str, value: str) -> float:
        if not value:
            return 0.0
        if value == token:
            return self.exact_score
        if value.startswith(token):
            return self.prefix_score
        if token in value:
            return self.substring_score

        # ratio() can never exceed 2 * min_len / total_len, so most pairs can be
        # rejected on length alone rather than by diffing them.
        if 2 * min(len(token), len(value)) < self.fuzzy_cutoff * (len(token) + len(value)):
            return 0.0

        matcher = SequenceMatcher(None, token, value)
        if matcher.quick_ratio() < self.fuzzy_cutoff:
            return 0.0
        ratio = matcher.ratio()
        return self.fuzzy_score * ratio if ratio >= self.fuzzy_cutoff else 0.0

    def token_score(self, token: str, icon: IconEntry) -> float:
        best = self.name_weight * self.match(token, icon.name)
        if icon.alias:
            best = max(best, self.name_weight * self.match(token, icon.alias))
        for value in icon.tags:
            best = max(best, self.field_weight * self.match(token, value.lower()))
        for value in icon.categories:
            best = max(best, self.field_weight * self.match(token, value.lower()))
        if icon.codepoint is not None and token == str(icon.codepoint):
            best = max(best, self.field_weight * self.exact_score)
        return best

    def score(self, query: str, icon: IconEntry) -> float:
        tokens = query.lower().split()

        total = 0.0
        for token in tokens:
            token_best = self.token_score(token, icon)
            if not token_best:
                return 0.0
            total += token_best

        # Ranks arrow-left above arrow-arc-left, which per-token scores tie.
        if len(tokens) > 1:
            total += self.name_weight * self.match("-".join(tokens), icon.name)

        return total


@cache
def get_ranking() -> Ranking:
    ranking = get_setting("ranking", Ranking)
    if isinstance(ranking, str):
        ranking = import_string(ranking)
    return ranking()
