from .normalizer import (
    normalize_whitespace,
    normalize_sections,
    mask_personal_attributes,
    normalize_resume,
)

from .fairness import (
    normalize_component_scores,
    reduce_keyword_dependence,
    calculate_bias_indicators,
    compare_scores,
    generate_fairness_evaluation,
)
