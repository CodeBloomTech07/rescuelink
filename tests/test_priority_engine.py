import pytest

from src.priority_engine import calculate_priority


def sample_report(**overrides):
    report = {
        "incident_id": "INC-001",
        "hazard_severity": 5,
        "people_affected": 80,
        "vulnerable_people": 20,
        "waiting_minutes": 120,
        "access_difficulty": 4,
        "reliability": 0.9,
    }
    report.update(overrides)
    return report


def test_score_is_within_zero_and_one_hundred():
    result = calculate_priority(sample_report())
    assert 0 <= result["priority_score"] <= 100


def test_high_severity_increases_priority():
    low = calculate_priority(
        sample_report(hazard_severity=1)
    )
    high = calculate_priority(
        sample_report(hazard_severity=5)
    )
    assert high["priority_score"] > low["priority_score"]


def test_low_reliability_does_not_reduce_urgency():
    trusted = calculate_priority(sample_report(reliability=0.95))
    uncertain = calculate_priority(sample_report(reliability=0.30))

    assert trusted["priority_score"] == uncertain["priority_score"]
    assert trusted["verification_required"] is False
    assert uncertain["verification_required"] is True


def test_explanation_contains_each_factor():
    result = calculate_priority(sample_report())
    assert len(result["explanations"]) == 5
    assert "hazard_severity" in result["factor_scores"]


def test_vulnerable_people_cannot_exceed_affected_people():
    with pytest.raises(ValueError):
        calculate_priority(
            sample_report(people_affected=10, vulnerable_people=11)
        )


def test_invalid_reliability_is_rejected():
    with pytest.raises(ValueError):
        calculate_priority(sample_report(reliability=1.5))


def test_same_input_produces_same_score():
    report = sample_report()
    assert calculate_priority(report) == calculate_priority(report)
