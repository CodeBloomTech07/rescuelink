"""Deterministic, capacity-aware resource allocation for RescueLink."""

from math import isfinite


def allocate_resources(incidents: list[dict], resources: list[dict]) -> dict:
    """
    Allocate available resources to incidents in descending priority order.

    Each resource can be assigned at most once. An incident can receive
    multiple resources of its required type. Resource capacity represents
    people served per deployment in this simulated scenario.

    This is a prototype heuristic, not a route optimizer.
    """
    incident_fields = {
        "incident_id", "priority_score", "people_affected",
        "required_resource_type",
    }
    resource_fields = {
        "resource_id", "resource_type", "capacity", "available",
    }

    seen_incidents = set()
    for incident in incidents:
        missing = incident_fields - incident.keys()
        if missing:
            raise ValueError(f"Incident missing fields: {sorted(missing)}")

        incident_id = str(incident["incident_id"]).strip()
        if not incident_id or incident_id in seen_incidents:
            raise ValueError("Incident IDs must be non-empty and unique.")
        seen_incidents.add(incident_id)

        score = incident["priority_score"]
        demand = incident["people_affected"]
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise ValueError("priority_score must be numeric.")
        if not isfinite(score) or not 0 <= score <= 100:
            raise ValueError("priority_score must be between 0 and 100.")
        if (isinstance(demand, bool) or not isinstance(demand, int)
                or demand < 1):
            raise ValueError("people_affected must be a positive integer.")
        if not str(incident["required_resource_type"]).strip():
            raise ValueError("required_resource_type cannot be empty.")

    seen_resources = set()
    for resource in resources:
        missing = resource_fields - resource.keys()
        if missing:
            raise ValueError(f"Resource missing fields: {sorted(missing)}")

        resource_id = str(resource["resource_id"]).strip()
        if not resource_id or resource_id in seen_resources:
            raise ValueError("Resource IDs must be non-empty and unique.")
        seen_resources.add(resource_id)

        capacity = resource["capacity"]
        if (isinstance(capacity, bool) or not isinstance(capacity, int)
                or capacity < 1):
            raise ValueError("Resource capacity must be a positive integer.")
        if not str(resource["resource_type"]).strip():
            raise ValueError("resource_type cannot be empty.")
        if not isinstance(resource["available"], bool):
            raise ValueError("available must be True or False.")

    available = {
        str(r["resource_id"]): r
        for r in resources if r["available"]
    }
    assignments = []
    incident_results = []

    ordered_incidents = sorted(
        incidents,
        key=lambda item: (-item["priority_score"], str(item["incident_id"]))
    )

    for incident in ordered_incidents:
        incident_id = str(incident["incident_id"])
        demand = incident["people_affected"]
        required_type = str(incident["required_resource_type"]).strip().casefold()
        assigned = []
        served = 0

        while served < demand:
            candidates = [
                resource for resource in available.values()
                if str(resource["resource_type"]).strip().casefold()
                == required_type
            ]
            if not candidates:
                break

            # Prefer the smallest resource that can finish the remaining
            # demand; otherwise use the largest available capacity.
            candidates.sort(key=lambda r: (
                0 if r["capacity"] >= demand - served else 1,
                r["capacity"] if r["capacity"] >= demand - served
                else -r["capacity"],
                str(r["resource_id"]),
            ))
            resource = candidates[0]
            resource_id = str(resource["resource_id"])
            del available[resource_id]

            served += resource["capacity"]
            assigned.append(resource_id)
            assignments.append({
                "incident_id": incident_id,
                "resource_id": resource_id,
                "resource_type": resource["resource_type"],
                "capacity": resource["capacity"],
            })

        incident_results.append({
            "incident_id": incident_id,
            "priority_score": incident["priority_score"],
            "people_affected": demand,
            "assigned_resource_ids": assigned,
            "capacity_assigned": served,
            "people_unserved": max(0, demand - served),
            "demand_met": served >= demand,
        })

    return {
        "assignments": assignments,
        "incident_results": incident_results,
        "unassigned_available_resources": sorted(available.keys()),
        "total_people_unserved": sum(
            item["people_unserved"] for item in incident_results
        ),
    }
