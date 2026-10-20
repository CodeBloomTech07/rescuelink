import pandas as pd
import streamlit as st

from src.echoshield import consolidate_reports
from src.priority_engine import calculate_priority
from src.rescueflow import allocate_resources
from src.stormshift import run_scenario


st.set_page_config(
    page_title="RescueLink | Command Center",
    page_icon="🚨",
    layout="wide",
)

st.markdown("""
<style>
.block-container {padding-top: 1.8rem; padding-bottom: 2rem;}
[data-testid="stMetric"] {
    background: rgba(128,128,128,0.08);
    padding: 16px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# SIMULATED FLOOD SCENARIO
# ---------------------------------------------------------

REPORTS = [
    {
        "report_id": "R-001",
        "area": "North Village",
        "description": "Flood water entering residential homes",
        "source": "Volunteer",
    },
    {
        "report_id": "R-002",
        "area": " north village ",
        "description": "FLOOD WATER ENTERING RESIDENTIAL HOMES!",
        "source": "Phone call",
    },
    {
        "report_id": "R-003",
        "area": "East Village",
        "description": "Bridge damaged and access restricted",
        "source": "Field team",
    },
    {
        "report_id": "R-004",
        "area": "Riverbank",
        "description": "Residents stranded by rising flood water",
        "source": "Volunteer",
    },
    {
        "report_id": "R-005",
        "area": "Hill Hamlet",
        "description": "Medical assistance requested for elderly residents",
        "source": "Community contact",
    },
]

RAW_INCIDENTS = [
    {
        "incident_id": "INC-001",
        "area": "North Village",
        "hazard_severity": 5,
        "people_affected": 80,
        "vulnerable_people": 20,
        "waiting_minutes": 120,
        "access_difficulty": 4,
        "reliability": 0.90,
        "required_resource_type": "boat",
        "remote": False,
    },
    {
        "incident_id": "INC-002",
        "area": "East Village",
        "hazard_severity": 4,
        "people_affected": 25,
        "vulnerable_people": 5,
        "waiting_minutes": 90,
        "access_difficulty": 5,
        "reliability": 0.80,
        "required_resource_type": "boat",
        "remote": False,
    },
    {
        "incident_id": "INC-003",
        "area": "Riverbank",
        "hazard_severity": 5,
        "people_affected": 40,
        "vulnerable_people": 12,
        "waiting_minutes": 45,
        "access_difficulty": 4,
        "reliability": 0.75,
        "required_resource_type": "boat",
        "remote": False,
    },
    {
        "incident_id": "INC-004",
        "area": "Hill Hamlet",
        "hazard_severity": 3,
        "people_affected": 12,
        "vulnerable_people": 9,
        "waiting_minutes": 150,
        "access_difficulty": 5,
        "reliability": 0.45,
        "required_resource_type": "ambulance",
        "remote": True,
    },
]

RESOURCES = [
    {
        "resource_id": "BOAT-01",
        "resource_type": "boat",
        "capacity": 50,
        "available": True,
    },
    {
        "resource_id": "BOAT-02",
        "resource_type": "boat",
        "capacity": 40,
        "available": True,
    },
    {
        "resource_id": "BOAT-03",
        "resource_type": "boat",
        "capacity": 20,
        "available": True,
    },
    {
        "resource_id": "AMB-01",
        "resource_type": "ambulance",
        "capacity": 10,
        "available": True,
    },
]

# These are invented demonstration values, not live emergency data.
PRIORITY_INCIDENTS = []

for raw in RAW_INCIDENTS:
    score_result = calculate_priority({
        "incident_id": raw["incident_id"],
        "hazard_severity": raw["hazard_severity"],
        "people_affected": raw["people_affected"],
        "vulnerable_people": raw["vulnerable_people"],
        "waiting_minutes": raw["waiting_minutes"],
        "access_difficulty": raw["access_difficulty"],
        "reliability": raw["reliability"],
    })

    PRIORITY_INCIDENTS.append({
        "incident_id": raw["incident_id"],
        "area": raw["area"],
        "priority_score": score_result["priority_score"],
        "priority_level": score_result["priority_level"],
        "people_affected": raw["people_affected"],
        "vulnerable_people": raw["vulnerable_people"],
        "reliability": raw["reliability"],
        "verification_required": score_result["verification_required"],
        "required_resource_type": raw["required_resource_type"],
        "remote": raw["remote"],
        "explanations": score_result["explanations"],
        "factor_scores": score_result["factor_scores"],
    })

BASELINE_INCIDENTS = [
    {
        "incident_id": item["incident_id"],
        "priority_score": item["priority_score"],
        "people_affected": item["people_affected"],
        "required_resource_type": item["required_resource_type"],
    }
    for item in PRIORITY_INCIDENTS
]


# ---------------------------------------------------------
# SIDEBAR: SCENARIO CONTROLS
# ---------------------------------------------------------

st.sidebar.title("🌊 Scenario controls")
st.sidebar.caption("SIMULATION MODE · No live emergency data")

resource_ids = [r["resource_id"] for r in RESOURCES]
resource_choice = st.sidebar.selectbox(
    "Simulate a resource outage",
    ["None"] + resource_ids,
)

add_emergency = st.sidebar.checkbox(
    "Simulate a new emergency report",
    value=False,
)

st.sidebar.divider()
st.sidebar.markdown("**Available resources in base scenario**")
for resource in RESOURCES:
    st.sidebar.write(
        f"{'🟢' if resource['available'] else '🔴'} "
        f"{resource['resource_id']} · {resource['capacity']} people"
    )

events = []

if resource_choice != "None":
    events.append({
        "type": "resource_unavailable",
        "resource_id": resource_choice,
    })

if add_emergency:
    new_report = {
        "incident_id": "INC-005",
        "hazard_severity": 5,
        "people_affected": 30,
        "vulnerable_people": 10,
        "waiting_minutes": 15,
        "access_difficulty": 4,
        "reliability": 0.65,
    }
    new_score = calculate_priority(new_report)

    events.append({
        "type": "new_incident",
        "incident": {
            "incident_id": "INC-005",
            "priority_score": new_score["priority_score"],
            "people_affected": new_report["people_affected"],
            "required_resource_type": "boat",
        },
    })


# ---------------------------------------------------------
# RUN THE ENGINES
# ---------------------------------------------------------

try:
    scenario = run_scenario(
        BASELINE_INCIDENTS,
        RESOURCES,
        events,
    )
except ValueError as exc:
    st.error(f"Scenario validation failed: {exc}")
    st.stop()

revised_result = scenario["revised"]
baseline_result = scenario["baseline"]

result_by_id = {
    item["incident_id"]: item
    for item in revised_result["incident_results"]
}

incident_details = {
    item["incident_id"]: item
    for item in PRIORITY_INCIDENTS
}

if add_emergency:
    incident_details["INC-005"] = {
        "incident_id": "INC-005",
        "area": "South Bank",
        "priority_score": new_score["priority_score"],
        "priority_level": new_score["priority_level"],
        "people_affected": 30,
        "vulnerable_people": 10,
        "reliability": 0.65,
        "verification_required": False,
        "required_resource_type": "boat",
        "remote": True,
        "explanations": new_score["explanations"],
        "factor_scores": new_score["factor_scores"],
    }


# ---------------------------------------------------------
# COMMAND CENTER
# ---------------------------------------------------------

st.title("🚨 RescueLink")
st.caption(
    "Smart Disaster Coordination & Resource Allocation"
    "  ·  Simulated flood response"
)

st.warning(
    "DEMO ONLY: All reports, resource capacities, scores and events "
    "are simulated. This dashboard does not dispatch emergency services."
)

unserved = revised_result["total_people_unserved"]
assigned_count = len(revised_result["assignments"])
verification_count = sum(
    1 for item in incident_details.values()
    if item["verification_required"]
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Incidents", len(incident_details))
m2.metric("Resource assignments", assigned_count)
m3.metric("People unserved", unserved)
m4.metric("Reports requiring review", verification_count)

if events:
    st.info(
        f"StormShift applied {len(events)} scenario event(s). "
        f"Unserved demand changed by {scenario['change_in_unserved']:+,} "
        "people compared with the base scenario."
    )

overview_tab, incidents_tab, resources_tab, equity_tab = st.tabs([
    "Command overview",
    "Incident intelligence",
    "Resource allocation",
    "Equity monitor",
])


# ---------------------------------------------------------
# TAB 1: OVERVIEW
# ---------------------------------------------------------

with overview_tab:
    left, right = st.columns([1.15, 1])

    with left:
        st.subheader("Incident priority queue")

        queue_rows = []
        for incident_id, detail in incident_details.items():
            allocation = result_by_id[incident_id]
            queue_rows.append({
                "Incident": incident_id,
                "Area": detail["area"],
                "Priority": detail["priority_score"],
                "Level": detail["priority_level"],
                "People affected": detail["people_affected"],
                "Unserved": allocation["people_unserved"],
            })

        queue_rows.sort(key=lambda row: -row["Priority"])
        st.dataframe(
            pd.DataFrame(queue_rows),
            hide_index=True,
            use_container_width=True,
        )

    with right:
        st.subheader("Report consolidation")

        consolidated = consolidate_reports(REPORTS)
        st.metric("Incoming reports", len(REPORTS))
        st.metric("Consolidated groups", len(consolidated))
        st.metric(
            "Potential duplicate reports",
            sum(
                group["report_count"] - 1
                for group in consolidated
            ),
        )

        st.caption(
            "EchoShield groups reports by normalized area and exact "
            "normalized description. Grouping is not proof that reports "
            "describe the same real-world incident."
        )

        st.subheader("Resource status")
        resource_rows = []
        for resource in RESOURCES:
            assigned = any(
                item["resource_id"] == resource["resource_id"]
                for item in revised_result["assignments"]
            )
            is_offline = (
                resource_choice == resource["resource_id"]
            )
            resource_rows.append({
                "Resource": resource["resource_id"],
                "Type": resource["resource_type"],
                "Capacity": resource["capacity"],
                "Status": (
                    "Offline (scenario)"
                    if is_offline
                    else "Assigned"
                    if assigned
                    else "Available"
                ),
            })

        st.dataframe(
            pd.DataFrame(resource_rows),
            hide_index=True,
            use_container_width=True,
        )


# ---------------------------------------------------------
# TAB 2: INCIDENT INTELLIGENCE
# ---------------------------------------------------------

with incidents_tab:
    st.subheader("Incident details and explanations")

    for incident_id, detail in sorted(
        incident_details.items(),
        key=lambda pair: -pair[1]["priority_score"],
    ):
        with st.expander(
            f"{incident_id} · {detail['area']} · "
            f"{detail['priority_score']:.1f}/100 · "
            f"{detail['priority_level']}"
        ):
            a, b, c = st.columns(3)
            a.metric("People affected", detail["people_affected"])
            b.metric("People unserved", result_by_id[incident_id]["people_unserved"])
            c.metric(
                "Report reliability",
                f"{detail['reliability']:.0%}",
            )

            st.markdown("**Priority factor contributions**")
            if "factor_scores" in detail:
                factor_frame = pd.DataFrame([
                    {
                        "Factor": name.replace("_", " ").title(),
                        "Factor score": round(value, 1),
                        "Weighted contribution": round(
                            value * {
                                "hazard_severity": 0.30,
                                "people_affected": 0.20,
                                "vulnerable_people": 0.20,
                                "waiting_time": 0.15,
                                "access_difficulty": 0.15,
                            }[name],
                            1,
                        ),
                    }
                    for name, value in detail["factor_scores"].items()
                ])
                st.dataframe(
                    factor_frame,
                    hide_index=True,
                    use_container_width=True,
                )

            if detail["verification_required"]:
                st.warning(
                    "Verification required. Low reliability does not "
                    "automatically reduce the urgency score."
                )

            st.markdown("**Resource recommendation**")
            assigned_ids = result_by_id[incident_id]["assigned_resource_ids"]
            st.write(
                ", ".join(assigned_ids)
                if assigned_ids
                else "No suitable available resource assigned."
            )

            st.markdown("**Demand status**")
            st.write(
                f"{result_by_id[incident_id]['capacity_assigned']} "
                f"capacity units assigned; "
                f"{result_by_id[incident_id]['people_unserved']} "
                "people remain unserved."
            )


# ---------------------------------------------------------
# TAB 3: RESOURCE ALLOCATION
# ---------------------------------------------------------

with resources_tab:
    st.subheader("RescueFlow allocation plan")

    st.caption(
        "Resources are assigned once each, in descending incident priority. "
        "Capacity is a simulated number of people served per deployment."
    )

    allocation_rows = []
    for item in revised_result["incident_results"]:
        detail = incident_details[item["incident_id"]]
        allocation_rows.append({
            "Incident": item["incident_id"],
            "Area": detail["area"],
            "Priority": item["priority_score"],
            "Required type": detail["required_resource_type"],
            "Assigned resources": (
                ", ".join(item["assigned_resource_ids"]) or "None"
            ),
            "Assigned capacity": item["capacity_assigned"],
            "People unserved": item["people_unserved"],
            "Demand met": item["demand_met"],
        })

    st.dataframe(
        pd.DataFrame(allocation_rows),
        hide_index=True,
        use_container_width=True,
    )

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Base vs revised scenario")
        comparison = pd.DataFrame([
            {
                "Scenario": "Base",
                "Assignments": len(baseline_result["assignments"]),
                "People unserved": baseline_result["total_people_unserved"],
            },
            {
                "Scenario": "Revised",
                "Assignments": len(revised_result["assignments"]),
                "People unserved": revised_result["total_people_unserved"],
            },
        ])
        st.dataframe(
            comparison,
            hide_index=True,
            use_container_width=True,
        )

    with col_b:
        st.subheader("Available but unassigned")
        unused = revised_result["unassigned_available_resources"]
        if unused:
            st.write(", ".join(unused))
        else:
            st.write("No available resources remain unassigned.")

    st.caption(
        "This prototype does not model travel distance, routes, "
        "simultaneous operations, resupply, or repeated deployments."
    )


# ---------------------------------------------------------
# TAB 4: EQUITY MONITOR
# ---------------------------------------------------------

with equity_tab:
    st.subheader("Resource equity and unmet needs")

    st.info(
        "A low report count is not evidence that a community is safe. "
        "These flags are prompts for human review, not definitive "
        "measurements of fairness."
    )

    reports_by_area = {}
    for report in REPORTS:
        area_key = " ".join(report["area"].casefold().split())
        reports_by_area[area_key] = reports_by_area.get(area_key, 0) + 1

    equity_rows = []
    for incident_id, detail in incident_details.items():
        allocation = result_by_id[incident_id]
        area_key = " ".join(detail["area"].casefold().split())

        # The new incident has one simulated incoming report.
        report_count = (
            1 if incident_id == "INC-005"
            else reports_by_area.get(area_key, 0)
        )

        flags = []
        if detail["remote"]:
            flags.append("Remote area")
        if report_count <= 1:
            flags.append("Sparse reporting")
        if allocation["people_unserved"] > 0:
            flags.append("Unmet demand")
        if detail["verification_required"]:
            flags.append("Verify report")

        equity_rows.append({
            "Area": detail["area"],
            "Reports received": report_count,
            "Remote": detail["remote"],
            "People affected": detail["people_affected"],
            "People unserved": allocation["people_unserved"],
            "Review flags": ", ".join(flags) if flags else "No current flags",
        })

    equity_frame = pd.DataFrame(equity_rows)
    st.dataframe(
        equity_frame,
        hide_index=True,
        use_container_width=True,
    )

    flagged = sum(
        row["Review flags"] != "No current flags"
        for row in equity_rows
    )
    st.metric("Areas flagged for human review", flagged)

    st.caption(
        "Reporting coverage is based only on the small simulated report "
        "dataset. A production system would need verified geographic "
        "coverage, population context and carefully validated equity metrics."
    )


st.divider()
st.caption(
    "RescueLink prototype · Rule-based recommendations · "
    "Simulated data · Human review required"
)
