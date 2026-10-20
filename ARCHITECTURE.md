# RescueLink — System Architecture

## 1. Project Overview

RescueLink is a simulation-based Smart Disaster Coordination and Resource Allocation prototype designed to demonstrate how emergency coordinators can organize incident reports, assess urgency, allocate limited resources, and adapt to changing disaster scenarios.

The current demonstration models a flood-response situation using simulated reports, incidents, resource capacities, and scenario events.

**Objective:** Provide a transparent, explainable decision-support workflow that helps coordinators understand incident priorities, resource assignments, and unmet demand.

## 2. Problem Statement

During disasters, responders may receive duplicate or uncertain reports while operating with limited rescue resources. Some incidents may require urgent attention, and some affected communities may remain underserved.

RescueLink demonstrates a structured workflow for:
- Consolidating potentially duplicate reports.
- Scoring and explaining incident priority.
- Recommending resource assignments under capacity constraints.
- Recalculating plans when simulated conditions change.
- Displaying unmet demand and equity-related indicators.

## 3. Technology Stack

- **Language:** Python
- **Dashboard:** Streamlit
- **Data handling:** pandas
- **Testing:** pytest
- **Version control:** Git and GitHub
- **Deployment:** Streamlit Community Cloud

## 4. System Modules

### 4.1 EchoShield — Report Consolidation

**File:** `src/echoshield.py`

EchoShield normalizes area names and report descriptions to group reports that appear to be duplicates.

The current approach uses normalized area and exact normalized description matching.

**Output:** Consolidated report groups and report counts.

**Limitation:** Similar wording is not proof that reports describe the same real-world event. The current method can miss differently worded duplicates or group distinct events that share matching text.

### 4.2 Priority Engine — Explainable Incident Scoring

**File:** `src/priority_engine.py`

The priority engine calculates an incident priority score and provides explanations of the contributing factors.

The dashboard displays the following weighted factors:

| Factor | Weight |
|---|---:|
| Hazard severity | 30% |
| People affected | 20% |
| Vulnerable people | 20% |
| Waiting time | 15% |
| Access difficulty | 15% |

The dashboard also displays report reliability and verification requirements separately from urgency.

**Design principle:** Uncertain information should be reviewed rather than automatically treated as evidence that an incident is less urgent.

These weights are prototype design choices, not validated emergency-response standards.

### 4.3 RescueFlow — Resource Allocation

**File:** `src/rescueflow.py`

RescueFlow generates a resource allocation plan using incident priorities, required resource types, and simulated resource capacities.

The current dashboard describes a heuristic approach in which resources are assigned once each, in descending incident priority order.

The resulting plan displays:
- Assigned resource identifiers.
- Assigned capacity.
- Estimated people served.
- People remaining unserved.
- Whether demand has been met.

**Limitation:** This is a simplified allocation heuristic, not a globally optimal logistics solver or a real-world dispatch system.

### 4.4 StormShift — Scenario Replanning

**File:** `src/stormshift.py`

StormShift evaluates simulated scenario changes and compares the baseline plan with a revised plan.

The dashboard supports demonstrations involving resource outages and the addition of a new emergency.

The comparison helps show how changes in available resources or incident demand can affect assignments and unmet demand.

**Limitation:** Scenario events and their outcomes are simulated; they do not represent live disaster conditions.

## 5. Dashboard Architecture

**Application entry point:** `app.py`

The Streamlit dashboard imports and uses the four core engine modules.

It contains four primary tabs:

1. **Command Overview:** Incident queue, report consolidation metrics, resource status, and high-level response indicators.
2. **Incident Intelligence:** Incident details, priority explanations, reliability, verification flags, and assignment summaries.
3. **Resource Allocation:** Assignment plan, capacity utilization, unmet demand, and baseline-versus-revised scenario comparisons.
4. **Equity Monitor:** Equity-related indicators intended to help identify potential gaps in response coverage.

Sidebar controls support scenario changes for demonstration purposes.

## 6. High-Level Data Flow

1. Simulated reports and incident data provide the scenario inputs.
2. EchoShield groups potentially duplicate reports.
3. The priority engine scores incidents and generates explanatory information.
4. RescueFlow produces a capacity-constrained resource allocation plan.
5. StormShift evaluates scenario changes and returns baseline and revised results.
6. Streamlit displays the resulting information for human review.

*Note: This is the intended high-level workflow. The exact execution order and dependencies should be verified against the engine calls in `app.py` and the individual module implementations.*

## 7. Repository Structure

```text
rescuelink/
├── app.py
├── src/
│   ├── __init__.py
│   ├── echoshield.py
│   ├── priority_engine.py
│   ├── rescueflow.py
│   └── stormshift.py
├── tests/
│   ├── __init__.py
│   ├── test_echoshield.py
│   ├── test_priority_engine.py
│   ├── test_rescueflow.py
│   └── test_stormshift.py
├── README.md
├── ARCHITECTURE.md
├── requirements.txt
└── .gitignore
```

## 8. Testing and Validation

The repository contains separate pytest modules for each core engine.

The previously completed test run reported **29 passing tests**. Tests should be rerun after future changes to confirm that the behavior remains correct.

Further validation should cover:
- Duplicate-report edge cases.
- Invalid or incomplete incident inputs.
- Resource-type compatibility.
- Capacity constraints and unmet demand.
- Resource outages and newly introduced incidents.
- Equity indicators and potentially underserved areas.

## 9. Scope, Assumptions, and Limitations

- Reports, locations, resource capacities, and scenario events are simulated and illustrative.
- Priority weights are explainable design choices, not clinically or operationally validated thresholds.
- Report consolidation is a baseline text-matching heuristic.
- Resource allocation is a simplified heuristic.
- The prototype does not perform automated emergency dispatch.
- It does not claim integration with live government emergency systems or real-time disaster feeds.
- Equity indicators are decision-support signals, not proof of discrimination or comprehensive fairness.
- Production use would require domain-expert validation, privacy and security controls, reliable geospatial services, audit logs, and extensive operational testing.

## 10. Future Development

Potential improvements include:
- More robust duplicate detection with human confirmation.
- Additional resource compatibility and scheduling constraints.
- Better visualization of geographic coverage and unmet demand.
- Scenario replay and audit history.
- Evaluation against carefully designed benchmark scenarios.
- Integration with verified external data sources in a controlled, secure environment.

## 11. Project Summary

RescueLink demonstrates a modular approach to simulated disaster coordination. It combines report consolidation, explainable incident prioritization, capacity-constrained resource recommendations, and scenario replanning in a single dashboard.

Its purpose is to support transparent decision-making and demonstrate a reproducible technical workflow. All recommendations remain simulated and require human review.
