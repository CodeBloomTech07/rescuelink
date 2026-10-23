# 🚨 RescueLink
### 🌍 Smart Disaster Coordination & Resource Allocation

<p align="center">
  <strong>When disaster strikes, every second matters.</strong>
  <br />
  An intelligent approach to incident prioritization, emergency resource coordination, and disaster-response planning.
</p>

<p align="center">
  <a href="https://rescuelinksim.lovable.app">
    <img src="https://img.shields.io/badge/🚨_COMMAND_CENTRE-Launch_RescueLink-0EA5E9?style=for-the-badge" alt="Launch RescueLink Command Centre" />
  </a>
  &nbsp;
  <a href="https://rescuelink.streamlit.app/">
    <img src="https://img.shields.io/badge/📊_STREAMLIT_DEMO-Explore_Prototype-FF4B4B?style=for-the-badge" alt="Explore RescueLink Streamlit Prototype" />
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Domain-Disaster_Response-DC2626?style=flat-square" alt="Disaster Response" />
  <img src="https://img.shields.io/badge/Language-Python_3-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3" />
  <img src="https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Data-Pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="Pandas" />
  <img src="https://img.shields.io/badge/Testing-Pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white" alt="Pytest" />
  <img src="https://img.shields.io/badge/Status-Prototype-64748B?style=flat-square" alt="Prototype" />
</p>

---

## ✨ Overview

**RescueLink** explores how disaster-response teams can coordinate information, prioritize urgent incidents, allocate limited resources, and adapt to rapidly changing conditions.

During floods, earthquakes, landslides, and other emergencies, response teams may face duplicate reports, inaccessible locations, competing medical needs, resource shortages, and uneven response coverage.

RescueLink brings these challenges into a structured decision-support workflow built around four core components:

- 🛡️ **EchoShield** — incident report consolidation
- 🎯 **Priority Engine** — transparent incident prioritization
- 🚑 **RescueFlow** — resource allocation
- 🌪️ **StormShift** — disruption-aware replanning

The project includes a Streamlit-based functional prototype and a separate disaster-response command-centre interface.

## 🌐 Explore RescueLink

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>🚨 Command Centre</h3>
      <p>A dedicated interface for disaster intelligence, incident monitoring, casualty prioritization, and emergency-response coordination.</p>
      <p><a href="https://rescuelinksim.lovable.app"><strong>↗ Launch Command Centre</strong></a></p>
    </td>
    <td width="50%" valign="top">
      <h3>📊 Streamlit Prototype</h3>
      <p>Explore the working prototype for incident consolidation, priority scoring, resource allocation, equity monitoring, and scenario replanning.</p>
      <p><a href="https://rescuelink.streamlit.app/"><strong>↗ Launch Streamlit Dashboard</strong></a></p>
    </td>
  </tr>
</table>

> **⚠️ Important:** The Streamlit dashboard uses simulated disaster-response data. The command-centre interface must not be assumed to have live emergency-service connectivity. These applications are not substitutes for verified emergency dispatch systems.

---

## 🎯 The Problem

Disaster response is not simply about identifying emergencies. It is about making difficult decisions when information is incomplete and resources are limited.

| Challenge | RescueLink approach |
|---|---|
| 🔁 Duplicate reports | Consolidate reports that match normalized locations and descriptions |
| 🚨 Competing emergencies | Prioritize incidents using transparent scoring factors |
| 🚑 Limited resources | Allocate available resources according to incident requirements and capacity |
| 🌪️ Changing conditions | Recalculate allocation plans after disruptions |
| 🗺️ Uneven response coverage | Highlight potential service gaps and unmet demand |
| 🔍 Difficult decisions | Make priority factors and allocation outputs easier to inspect |

## ⚙️ Core Modules

### 🛡️ 01 — EchoShield
**Incident Report Consolidation**

Identifies potential duplicate reports by comparing normalized area names and descriptions.

- 🔎 Normalizes report text for comparison
- 🔗 Groups matching reports
- 📋 Helps reduce duplicate entries in the incident workflow

*Matching reports are potential duplicates, not confirmed instances of the same real-world event.*

### 🎯 02 — Priority Engine
**Transparent Incident Prioritization**

Evaluates incidents using a weighted set of factors:

- 🔥 Hazard severity
- 👥 Number of people affected
- 🩺 Vulnerable people
- ⏱️ Waiting time
- 🛣️ Accessibility difficulty

The objective is to make prioritization more explainable than an opaque ranking.

### 🚑 03 — RescueFlow
**Resource Allocation**

Allocates available resources using incident priority, resource type, and capacity.

- 📦 Considers resource availability and requirements
- 🎯 Connects higher-priority incidents with suitable resources
- 📊 Produces allocation outputs for review

### 🌪️ 04 — StormShift
**Disruption-Aware Replanning**

Explores how response plans can change when operational conditions change.

- 🚧 Handles simulated resource outages
- 🆕 Incorporates new emergency reports
- 🔄 Recalculates allocation plans
- 📈 Supports comparison between baseline and revised plans

### ⚖️ 05 — Equity Monitoring
**Identifying Potential Response Gaps**

Highlights conditions that may warrant additional attention:

- 🏘️ Remote or difficult-to-access locations
- 📉 Potentially unmet demand
- 📡 Sparse reporting
- 🔍 Incidents requiring verification

These indicators are preliminary decision-support signals, not proof of discrimination or neglect.

---

## 🧠 How It Works

<p align="center">
  <strong>📥 REPORTS → 🛡️ ECHOSHIELD → 🎯 PRIORITY ENGINE → 🚑 RESCUEFLOW</strong>
  <br />
  <strong>⬆️ 🌪️ STORMSHIFT RECALCULATES PLANS WHEN CONDITIONS CHANGE</strong>
</p>

1. **📥 Collect:** Incident reports and resource information enter the workflow.
2. **🛡️ Consolidate:** Potential duplicate reports are grouped.
3. **🎯 Prioritize:** Incidents are ranked using documented scoring factors.
4. **🚑 Allocate:** Available resources are assigned according to priority and suitability.
5. **🌪️ Replan:** Changes in conditions trigger revised allocation plans.
6. **⚖️ Review:** Potential service gaps and unmet demand are highlighted.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| 🐍 Python 3 | Core application logic |
| 📊 Streamlit | Interactive prototype dashboard |
| 🐼 Pandas | Data handling and analysis |
| 🧪 Pytest | Automated testing |
| 🌿 Git | Version control |
| 🐙 GitHub | Source-code hosting |
| ☁️ Streamlit Community Cloud | Prototype deployment |
| 🎨 Lovable | Command-centre interface |

## 📁 Project Structure

```text
rescuelink/
│
├── app.py                  # Streamlit application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── ARCHITECTURE.md         # System design and module descriptions
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── echoshield.py       # Report consolidation
│   ├── priority_engine.py  # Incident priority scoring
│   ├── rescueflow.py       # Resource allocation
│   └── stormshift.py       # Disruption and replanning
│
└── tests/
    ├── __init__.py
    ├── test_echoshield.py
    ├── test_priority_engine.py
    ├── test_rescueflow.py
    └── test_stormshift.py
```

## 🚀 Run Locally

### Prerequisites

- Python 3
- Git
- A terminal

### ① Clone the repository

```bash
git clone https://github.com/CodeBloomTech07/rescuelink.git
cd rescuelink
```

### ② Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### ③ Install dependencies

```bash
python -m pip install -r requirements.txt
```

### ④ Launch RescueLink

```bash
python -m streamlit run app.py
```

Open the local URL printed in the terminal, usually:

**http://localhost:8501**

### ⑤ Run the test suite

```bash
python -m pytest -v
```

## 🧪 Explore the Prototype

Once the dashboard is running:

1. 📋 Review incident reports and the priority queue.
2. 🔎 Inspect incident priority factors.
3. 🚧 Trigger a resource outage using the available controls.
4. 🆕 Toggle the new emergency report.
5. 🔄 Compare baseline and revised allocation plans.
6. ⚖️ Review the equity monitor for potential service gaps.

## 🧪 Testing & Validation

The project has previously recorded **29 passing automated tests**, along with manual checks of the dashboard's main interactions.

These are historical test results and should be rerun against the current repository to confirm its present status.

Testing verifies software behavior under the tested conditions; it does not establish real-world disaster-response effectiveness.

## ⚠️ Limitations

- 📡 The Streamlit prototype uses simulated data, not verified live incident feeds.
- 🔎 Text-based report matching cannot confirm that two reports describe the same event.
- 🎯 Priority scores are prototype heuristics, not validated disaster-response standards.
- 🚑 Allocation results are planning outputs, not confirmed emergency deployments.
- ⚖️ Equity indicators are preliminary and require contextual review.
- 📍 Live GPS tracking, verified external incident feeds, and confirmed emergency-service dispatch integrations are not implemented in the Streamlit prototype.

## 🔭 Future Development

- 📡 Integration with verified external incident data sources
- 🧠 More robust report similarity and human-verification workflows
- 🚑 Improved resource-allocation algorithms
- ⚖️ Expanded fairness and accessibility evaluation
- 🧾 Detailed decision audit trails
- 🗺️ Enhanced geographic visualization and route analysis
- 🧪 Broader automated testing and documented evaluation scenarios
- 🔗 Verified integrations with emergency-response systems

## 🏁 Project Status

**Functional disaster-response coordination prototype with a separate command-centre interface.**

RescueLink explores how transparent prioritization, resource coordination, and adaptive planning can contribute to more structured disaster-response workflows.

---

<p align="center">
  <strong>🚨 RescueLink — Coordinating information. Prioritizing needs. Connecting resources.</strong>
  <br />
  <sub>Built as a disaster-response coordination and decision-support project.</sub>
</p>
