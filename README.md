# RescueLink 🚨
### Smart Disaster Coordination & Resource Allocation

RescueLink is a simulation-based disaster response coordination prototype designed to demonstrate how incident reports, transparent priority scoring, resource allocation, and scenario replanning can work together during a simulated flood response.

> **Demo only:** All incident reports, people counts, resource capacities, priority scores, and scenario events are simulated. RescueLink does not dispatch emergency services or provide validated real-world emergency recommendations.

## Live Demo

Explore the deployed RescueLink simulation:

**[Open RescueLink Dashboard](https://rescuelink.streamlit.app/)**

The dashboard uses simulated disaster-response data. It is intended for demonstration and experimentation, not real emergency dispatch.

For the system design and module descriptions, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Problem Statement

During a disaster, response teams may face duplicate reports, limited resources, competing priorities, changing conditions, and communities whose needs are easy to overlook.

RescueLink explores a structured, explainable approach to these challenges through a small, testable decision-support prototype.

## Core Features

- **Report consolidation (EchoShield):** Groups reports with matching normalized area names and descriptions to identify potential duplicates.
- **Transparent priority scoring:** Combines hazard severity, people affected, vulnerable people, waiting time, and access difficulty.
- **Resource allocation (RescueFlow):** Assigns available resources according to incident priority, resource type, and capacity.
- **Scenario replanning (StormShift):** Recalculates allocations after simulated resource outages or the arrival of a new incident.
- **Equity monitoring:** Highlights unmet demand, remote locations, sparse reporting, and incidents requiring verification.
- **Interactive dashboard:** Provides a Streamlit interface for exploring the simulated response and changing scenario conditions.
- **Automated tests:** Checks core behavior, validation, and repeatability.

## Technology Stack

- Python 3
- Streamlit
- Pandas
- Pytest
- Git and GitHub
- Streamlit Community Cloud for deployment

## Project Structure

```text
rescuelink/
├── app.py
├── requirements.txt
├── README.md
├── ARCHITECTURE.md
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── echoshield.py
│   ├── priority_engine.py
│   ├── rescueflow.py
│   └── stormshift.py
└── tests/
    ├── __init__.py
    ├── test_echoshield.py
    ├── test_priority_engine.py
    ├── test_rescueflow.py
    └── test_stormshift.py
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/CodeBloomTech07/rescuelink.git
cd rescuelink
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Launch the dashboard

```bash
python -m streamlit run app.py
```

Open the local URL printed by Streamlit, usually:

`http://localhost:8501`

### 5. Run the automated tests

```bash
python -m pytest -v
```

## Exploring the Simulation

1. Review the incident priority queue and report consolidation.
2. Open the incident intelligence tab to inspect priority factors.
3. Simulate a resource outage using the sidebar.
4. Toggle the new emergency report.
5. Compare the baseline and revised allocation plans.
6. Review the equity monitor for potential service gaps.

## Current Limitations

- Uses simulated data rather than live incident feeds.
- Report consolidation uses normalized text matching; it does not establish whether reports describe the same real-world event.
- Priority scores are prototype heuristics, not validated disaster response standards.
- Resource assignments are planning outputs, not confirmed deployments.
- Equity indicators are preliminary flags and do not establish that a community is being discriminated against or neglected.
- No live GPS tracking, emergency-service integration, or dispatch functionality is implemented.

## Future Development

Potential next steps include:

- Externalizing sample incidents and resources into documented datasets.
- Improving report similarity analysis and human verification workflows.
- Expanding allocation and fairness tests.
- Adding clearer scenario comparison and audit trails.
- Evaluating the prototype with documented assumptions and synthetic test scenarios.
- Exploring deployment as a public demonstration.

## Testing Status

The local automated test suite has previously passed **29 tests**.

The dashboard's main interactions have also passed manual checks.

These results verify prototype behavior only; they do not establish real-world emergency response effectiveness.

## Project Status

**Early-stage functional prototype — simulation and demonstration only.**
