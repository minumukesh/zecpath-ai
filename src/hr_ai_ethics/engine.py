from datetime import datetime, timezone, timedelta

from .config import SENSITIVE_FIELDS, DEFAULT_RETENTION_DAYS


def validate_consent(record):
    required = [
        "consent_given",
        "purpose",
        "consent_timestamp",
        "policy_version"
    ]

    missing = [key for key in required if key not in record]

    if missing:
        return {
            "valid": False,
            "status": "INCOMPLETE",
            "missing_fields": missing
        }

    if record["consent_given"] is not True:
        return {
            "valid": False,
            "status": "CONSENT_NOT_GRANTED",
            "missing_fields": []
        }

    if record.get("withdrawn", False):
        return {
            "valid": False,
            "status": "CONSENT_WITHDRAWN",
            "missing_fields": []
        }

    if not str(record["purpose"]).strip():
        return {
            "valid": False,
            "status": "PURPOSE_REQUIRED",
            "missing_fields": []
        }

    if not str(record["policy_version"]).strip():
        return {
            "valid": False,
            "status": "POLICY_VERSION_REQUIRED",
            "missing_fields": []
        }

    try:
        datetime.fromisoformat(
            str(record["consent_timestamp"]).replace("Z", "+00:00")
        )
    except ValueError:
        return {
            "valid": False,
            "status": "INVALID_TIMESTAMP",
            "missing_fields": []
        }

    return {
        "valid": True,
        "status": "CONSENT_VALID",
        "missing_fields": []
    }


def remove_demographic_signals(data):
    if not isinstance(data, dict):
        raise ValueError("Candidate data must be a dictionary.")

    cleaned = {}
    removed = []

    for key, value in data.items():
        normalized = str(key).strip().lower()

        if normalized in SENSITIVE_FIELDS:
            removed.append(key)
            continue

        if isinstance(value, dict):
            nested = remove_demographic_signals(value)
            cleaned[key] = nested["cleaned_data"]
            removed.extend(nested["removed_fields"])
        else:
            cleaned[key] = value

    return {
        "cleaned_data": cleaned,
        "removed_fields": removed,
        "removed_count": len(removed)
    }


def generate_explainability_notes(component_scores, weights, final_score):
    final_score = float(final_score)

    if not 0 <= final_score <= 100:
        raise ValueError("Final score must be between 0 and 100.")

    notes = []

    for component, score in component_scores.items():
        if score is None:
            notes.append(component + ": score unavailable.")
            continue

        value = float(score)

        if not 0 <= value <= 100:
            raise ValueError("Invalid component score.")

        weight = float(weights.get(component, 0))

        notes.append(
            component + ": score " + str(value)
            + ", configured weight " + str(weight) + "%."
        )

    notes.append("Final recorded score: " + str(final_score) + ".")
    notes.append(
        "These notes explain recorded scoring inputs. "
        "They do not guarantee future job performance."
    )

    return {
        "final_score": round(final_score, 2),
        "component_notes": notes
    }


def audit_group_fairness(outcomes, minimum_group_size=5):
    if minimum_group_size < 1:
        raise ValueError("Minimum group size must be positive.")

    groups = {}

    for row in outcomes:
        group = str(row.get("audit_group", "UNKNOWN"))
        selected = row.get("selected")

        if not isinstance(selected, bool):
            raise ValueError("Selection outcome must be boolean.")

        groups.setdefault(group, []).append(selected)

    summary = {}
    rates = []

    for group, values in groups.items():
        total = len(values)

        if total < minimum_group_size:
            summary[group] = {
                "sample_size": total,
                "selection_rate": None,
                "status": "INSUFFICIENT_SAMPLE"
            }
            continue

        rate = sum(values) / total
        rates.append(rate)

        summary[group] = {
            "sample_size": total,
            "selected_count": sum(values),
            "selection_rate": round(rate * 100, 2),
            "status": "AUDITABLE"
        }

    if len(rates) >= 2:
        gap = round((max(rates) - min(rates)) * 100, 2)
        status = "REVIEW_REQUIRED"
    else:
        gap = None
        status = "INSUFFICIENT_GROUP_DATA"

    return {
        "groups": summary,
        "selection_rate_gap_percentage_points": gap,
        "status": status,
        "warning": (
            "A selection-rate difference is an audit signal, "
            "not proof of discrimination."
        )
    }


def check_data_retention(
    created_at,
    retention_days=DEFAULT_RETENTION_DAYS,
    now=None,
    consent_withdrawn=False
):
    if retention_days < 0:
        raise ValueError("Retention days cannot be negative.")

    try:
        created = datetime.fromisoformat(
            str(created_at).replace("Z", "+00:00")
        )
    except ValueError:
        raise ValueError("Invalid creation timestamp.")

    if created.tzinfo is None:
        created = created.replace(tzinfo=timezone.utc)

    current = now or datetime.now(timezone.utc)

    if current.tzinfo is None:
        current = current.replace(tzinfo=timezone.utc)

    expiry = created + timedelta(days=retention_days)
    expired = current >= expiry

    if consent_withdrawn:
        status = "REVIEW_FOR_EARLY_DELETION"
    elif expired:
        status = "RETENTION_EXPIRED"
    else:
        status = "WITHIN_RETENTION_PERIOD"

    return {
        "created_at": created.isoformat(),
        "retention_days": retention_days,
        "expiry_date": expiry.isoformat(),
        "expired": expired,
        "consent_withdrawn": consent_withdrawn,
        "status": status,
        "deletion_action": (
            "ELIGIBLE_FOR_PURGE_REVIEW"
            if expired or consent_withdrawn
            else "RETAIN_UNTIL_EXPIRY"
        )
    }


def generate_compliance_report(consent, fairness, retention):
    checks = {
        "consent": consent["valid"],
        "fairness_review": fairness["status"] == "AUDITABLE",
        "retention": retention["status"] in (
            "WITHIN_RETENTION_PERIOD",
            "RETENTION_EXPIRED",
            "REVIEW_FOR_EARLY_DELETION"
        )
    }

    return {
        "checks": checks,
        "completed_checks": sum(checks.values()),
        "total_checks": len(checks),
        "readiness_status": (
            "CHECKS_PASSED" if all(checks.values())
            else "REVIEW_REQUIRED"
        ),
        "notice": (
            "Technical readiness report only. "
            "It is not legal certification."
        )
    }
