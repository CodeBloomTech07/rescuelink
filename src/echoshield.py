import re
from collections import defaultdict


def normalize_area(area: str) -> str:
    """Normalize an area label for comparison."""
    return " ".join(area.casefold().split())


def normalize_description(description: str) -> str:
    """Normalize basic punctuation and whitespace."""
    text = description.casefold()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return " ".join(text.split())


def consolidate_reports(reports: list[dict]) -> list[dict]:
    """
    Baseline EchoShield:
    group reports with the same normalized area and exact normalized
    description. Preserve every original report ID.

    This deliberately conservative baseline does not claim to detect
    all semantic duplicates or determine whether reports are true.
    """
    groups = defaultdict(list)

    for report in reports:
        required = {"report_id", "area", "description"}
        missing = required - report.keys()
        if missing:
            raise ValueError(f"Report missing required fields: {sorted(missing)}")

        report_id = str(report["report_id"]).strip()
        area = str(report["area"]).strip()
        description = str(report["description"]).strip()

        if not report_id or not area or not description:
            raise ValueError("Report ID, area, and description cannot be empty.")

        key = (normalize_area(area), normalize_description(description))
        groups[key].append(report)

    incidents = []

    for index, ((area_key, description_key), group) in enumerate(
        groups.items(), start=1
    ):
        incidents.append({
            "incident_id": f"INC-{index:03d}",
            "area_key": area_key,
            "description_key": description_key,
            "report_ids": [str(r["report_id"]).strip() for r in group],
            "report_count": len(group),
            "potential_duplicate": len(group) > 1,
        })

    return incidents
