import pytest

from src.echoshield import consolidate_reports


def test_identical_reports_are_grouped():
    reports = [
        {"report_id": "R1", "area": "North Village",
         "description": "Flood water entered homes!"},
        {"report_id": "R2", "area": " north village ",
         "description": "FLOOD WATER ENTERED HOMES"},
    ]

    incidents = consolidate_reports(reports)

    assert len(incidents) == 1
    assert incidents[0]["report_count"] == 2
    assert set(incidents[0]["report_ids"]) == {"R1", "R2"}
    assert incidents[0]["potential_duplicate"] is True


def test_different_descriptions_remain_separate():
    reports = [
        {"report_id": "R1", "area": "North Village",
         "description": "Bridge collapsed"},
        {"report_id": "R2", "area": "North Village",
         "description": "People trapped in homes"},
    ]

    assert len(consolidate_reports(reports)) == 2


def test_empty_input_returns_no_incidents():
    assert consolidate_reports([]) == []


def test_missing_required_field_is_rejected():
    with pytest.raises(ValueError):
        consolidate_reports([
            {"report_id": "R1", "area": "North Village"}
        ])


def test_empty_report_values_are_rejected():
    with pytest.raises(ValueError):
        consolidate_reports([
            {"report_id": "R1", "area": " ", "description": "Flooding"}
        ])
