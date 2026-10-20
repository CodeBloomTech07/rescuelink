"""Explainable, rule-based incident prioritization for RescueLink."""

from math import isfinite


WEIGHTS = {
    "hazard_severity": 0.30,
    "people_affected": 0.20,
    "vulnerable_people": 0.20,
    "waiting_time": 0.15,
    "access_difficulty": 0.15,
}


def _validate(report):
    required = {
        "incident_id",
        "hazard_severity",
        "people_affected",
        "vulnerable_people",
        "waiting_minutes",
        "access_difficulty",
        "reliability",
    }
    missing = required - report.keys()
    if missing:
        raise ValueError(f"Missing fields: {sorted(missing)}")

    for field in (
        "hazard_severity",
        "people_affected",
        "vulnerable_people",
        "waiting_minutes",
        "access_difficulty",
    ):
        value = report[field]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{field} must be numeric.")
        if not isfinite(value):
            raise ValueError(f"{field} must be finite.")

    for field in (
        "hazard_severity",
        "people_affected",
        "vulnerable_people",
        "waiting_minutes",
        "access_difficulty",
    ):
        if report[field] < 0:
            raise ValueError(f"{field} cannot be negative.")

    if not 1 <= report["hazard_severity"] <= 5:
        raise ValueError("hazard_severity must be between 1 and 5.")
    if not 1 <= report["access_difficulty"] <= 5:
        raise ValueError("access_difficulty must be between 1 and 5.")
    if not float(report["people_affected"]).is_integer():
        raise ValueError("people_affected must be an integer.")
    if not float(report["vulnerable_people"]).is_integer():
        raise ValueError("vulnerable_people must be an integer.")
    if not float(report["waiting_minutes"]).is_integer():
        raise ValueError("waiting_minutes must be an integer.")
    if report["people_affected"] < 1:
        raise ValueError("people_affected must be at least 1.")
    if report["vulnerable_people"] > report["people_affected"]:
        raise ValueError("Vulnerable people cannot exceed people affected.")
    if not 0 <= report["reliability"] <= 1:
        raise ValueError("reliability must be between 0 and 1.")


def calculate_priority(report):
    """Return a reproducible score, factor breakdown and review flags."""
    _validate(report)

    people = report["people_affected"]
    vulnerable = report["vulnerable_people"]

    factors = {
        "hazard_severity": report["hazard_severity"] / 5 * 100,
        "people_affected": min(people, 100) / 100 * 100,
        "vulnerable_people": vulnerable / people * 100,
        "waiting_time": min(report["waiting_minutes"], 240) / 240 * 100,
        "access_difficulty": report["access_difficulty"] / 5 * 100,
    }

    contributions = {
        name: value * WEIGHTS[name]
        for name, value in factors.items()
    }
    score = round(sum(contributions.values()), 2)

    if score >= 70:
        level = "High"
    elif score >= 40:
        level = "Medium"
    else:
        level = "Low"

    reliability = report["reliability"]
    review_required = reliability < 0.60

    explanations = [
        f"{name.replace('_', ' ').title()}: "
        f"{factors[name]:.1f}/100, contributing "
        f"{contributions[name]:.1f} points."
        for name in WEIGHTS
    ]

    if review_required:
        explanations.append(
            "Verification required: report reliability is below 0.60. "
            "This does not reduce the urgency score."
        )

    return {
        "incident_id": str(report["incident_id"]),
        "priority_score": score,
        "priority_level": level,
        "factor_scores": factors,
        "contributions": contributions,
        "reliability": reliability,
        "verification_required": review_required,
        "explanations": explanations,
    }
