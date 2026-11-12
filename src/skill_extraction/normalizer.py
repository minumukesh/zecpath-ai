from .skill_dictionary import ALL_SKILLS, SPELLING_VARIATIONS


def normalize_skill(skill):
    """Convert a skill variation into its canonical name."""

    skill = skill.lower().strip()

    if skill in SPELLING_VARIATIONS:
        skill = SPELLING_VARIATIONS[skill]

    for category, skills in ALL_SKILLS.items():

        for canonical, aliases in skills.items():

            if skill == canonical.lower():
                return canonical

            if skill in [alias.lower() for alias in aliases]:
                return canonical

    return skill


def build_alias_lookup():
    """Create alias -> canonical skill mapping."""

    lookup = {}

    for category, skills in ALL_SKILLS.items():

        for canonical, aliases in skills.items():

            lookup[canonical.lower()] = canonical

            for alias in aliases:
                lookup[alias.lower()] = canonical

    return lookup


SKILL_ALIAS_LOOKUP = build_alias_lookup()
