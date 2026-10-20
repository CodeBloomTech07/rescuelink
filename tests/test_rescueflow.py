import pytest

from src.rescueflow import allocate_resources


def incident(incident_id="INC-001", priority=80, people=8, kind="boat"):
    return {
        "incident_id": incident_id,
        "priority_score": priority,
        "people_affected": people,
        "required_resource_type": kind,
    }


def resource(resource_id="BOAT-1", capacity=10, kind="boat",
             available=True):
    return {
        "resource_id": resource_id,
        "resource_type": kind,
        "capacity": capacity,
        "available": available,
    }


def test_sufficient_capacity_meets_demand():
    result = allocate_resources(
        [incident(people=8)],
        [resource(capacity=10)],
    )
    row = result["incident_results"][0]
    assert row["demand_met"] is True
    assert row["people_unserved"] == 0


def test_multiple_resources_can_cover_one_incident():
    result = allocate_resources(
        [incident(people=12)],
        [
            resource("BOAT-1", 5),
            resource("BOAT-2", 7),
        ],
    )
    row = result["incident_results"][0]
    assert len(row["assigned_resource_ids"]) == 2
    assert row["demand_met"] is True


def test_unavailable_resource_is_never_assigned():
    result = allocate_resources(
        [incident()],
        [resource(available=False)],
    )
    assert result["assignments"] == []
    assert result["total_people_unserved"] == 8


def test_incompatible_resource_type_is_not_assigned():
    result = allocate_resources(
        [incident(kind="ambulance")],
        [resource(kind="boat")],
    )
    assert result["assignments"] == []
    assert result["incident_results"][0]["people_unserved"] == 8


def test_higher_priority_incident_is_served_first():
    result = allocate_resources(
        [
            incident("INC-LOW", priority=30, people=8),
            incident("INC-HIGH", priority=90, people=8),
        ],
        [resource("BOAT-1", capacity=8)],
    )
    rows = {r["incident_id"]: r for r in result["incident_results"]}
    assert rows["INC-HIGH"]["demand_met"] is True
    assert rows["INC-LOW"]["people_unserved"] == 8


def test_resource_is_never_assigned_twice():
    result = allocate_resources(
        [
            incident("INC-1", priority=80, people=5),
            incident("INC-2", priority=60, people=5),
        ],
        [resource("BOAT-1", capacity=5)],
    )
    assigned_ids = [a["resource_id"] for a in result["assignments"]]
    assert len(assigned_ids) == len(set(assigned_ids))


def test_invalid_capacity_is_rejected():
    with pytest.raises(ValueError):
        allocate_resources(
            [incident()],
            [resource(capacity=0)],
        )


def test_duplicate_resource_ids_are_rejected():
    with pytest.raises(ValueError):
        allocate_resources(
            [incident()],
            [resource("BOAT-1"), resource("BOAT-1")],
        )


def test_same_inputs_produce_same_output():
    incidents = [incident()]
    resources = [resource()]
    assert allocate_resources(incidents, resources) == (
        allocate_resources(incidents, resources)
    )
