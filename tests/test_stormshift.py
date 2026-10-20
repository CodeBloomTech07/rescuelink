import pytest

from src.stormshift import run_scenario


def make_incident(incident_id="INC-1", priority=80, people=8):
    return {
        "incident_id": incident_id,
        "priority_score": priority,
        "people_affected": people,
        "required_resource_type": "boat",
    }


def make_resource(resource_id="BOAT-1", capacity=8, available=True):
    return {
        "resource_id": resource_id,
        "resource_type": "boat",
        "capacity": capacity,
        "available": available,
    }


def test_resource_outage_recalculates_plan():
    result = run_scenario(
        [make_incident()],
        [make_resource()],
        [{"type": "resource_unavailable", "resource_id": "BOAT-1"}],
    )
    assert len(result["baseline"]["assignments"]) == 1
    assert result["revised"]["assignments"] == []
    assert result["unserved_after"] == 8


def test_new_incident_is_included_in_revised_plan():
    result = run_scenario(
        [make_incident()],
        [make_resource("BOAT-1"), make_resource("BOAT-2")],
        [{
            "type": "new_incident",
            "incident": make_incident("INC-2", priority=95),
        }],
    )
    revised_ids = {
        row["incident_id"]
        for row in result["revised"]["incident_results"]
    }
    assert revised_ids == {"INC-1", "INC-2"}


def test_original_inputs_are_not_mutated():
    incidents = [make_incident()]
    resources = [make_resource()]
    original_resources = [dict(item) for item in resources]

    run_scenario(
        incidents,
        resources,
        [{"type": "resource_unavailable", "resource_id": "BOAT-1"}],
    )

    assert resources == original_resources


def test_unknown_resource_is_rejected():
    with pytest.raises(ValueError):
        run_scenario(
            [make_incident()],
            [make_resource()],
            [{"type": "resource_unavailable", "resource_id": "BOAT-99"}],
        )


def test_duplicate_new_incident_id_is_rejected():
    with pytest.raises(ValueError):
        run_scenario(
            [make_incident()],
            [make_resource()],
            [{
                "type": "new_incident",
                "incident": make_incident("INC-1"),
            }],
        )


def test_unknown_event_is_rejected():
    with pytest.raises(ValueError):
        run_scenario(
            [make_incident()],
            [make_resource()],
            [{"type": "teleport_resource"}],
        )


def test_replanning_is_deterministic():
    incidents = [make_incident()]
    resources = [make_resource()]
    events = [
        {"type": "resource_unavailable", "resource_id": "BOAT-1"}
    ]
    assert run_scenario(incidents, resources, events) == (
        run_scenario(incidents, resources, events)
    )


def test_no_events_preserve_allocation():
    result = run_scenario(
        [make_incident()],
        [make_resource()],
        [],
    )
    assert result["baseline"] == result["revised"]
    assert result["change_in_unserved"] == 0
