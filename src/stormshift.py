"""Scenario simulation and replanning for RescueLink."""

from copy import deepcopy

from src.rescueflow import allocate_resources


def run_scenario(incidents: list[dict],
                 resources: list[dict],
                 events: list[dict]) -> dict:
    """
    Apply simulated events to copies of the scenario and recalculate
    resource recommendations.

    Supported event types:
      - resource_unavailable: {"type": ..., "resource_id": ...}
      - new_incident: {"type": ..., "incident": {...}}
    """
    updated_incidents = deepcopy(incidents)
    updated_resources = deepcopy(resources)
    applied_events = []

    for event in events:
        event_type = event.get("type")

        if event_type == "resource_unavailable":
            resource_id = str(event.get("resource_id", "")).strip()
            matches = [
                resource for resource in updated_resources
                if str(resource["resource_id"]) == resource_id
            ]

            if not resource_id or not matches:
                raise ValueError(
                    f"Unknown resource ID: {resource_id or '(empty)'}"
                )

            matches[0]["available"] = False
            applied_events.append({
                "type": event_type,
                "resource_id": resource_id,
            })

        elif event_type == "new_incident":
            new_item = event.get("incident")
            if not isinstance(new_item, dict):
                raise ValueError("new_incident requires an incident dictionary.")

            new_id = str(new_item.get("incident_id", "")).strip()
            existing_ids = {
                str(item["incident_id"]) for item in updated_incidents
            }
            if not new_id:
                raise ValueError("New incident must have a non-empty ID.")
            if new_id in existing_ids:
                raise ValueError(f"Incident ID already exists: {new_id}")

            updated_incidents.append(deepcopy(new_item))
            applied_events.append({
                "type": event_type,
                "incident_id": new_id,
            })

        else:
            raise ValueError(f"Unsupported scenario event: {event_type}")

    # Validate the resulting scenario and generate new recommendations.
    baseline = allocate_resources(incidents, resources)
    revised = allocate_resources(updated_incidents, updated_resources)

    return {
        "baseline": baseline,
        "revised": revised,
        "applied_events": applied_events,
        "unserved_before": baseline["total_people_unserved"],
        "unserved_after": revised["total_people_unserved"],
        "change_in_unserved": (
            revised["total_people_unserved"]
            - baseline["total_people_unserved"]
        ),
    }
