# UAV-Strategic-Deconfliction

## Overview

This project implements a strategic deconfliction system for UAV (drone) waypoint missions operating in shared airspace. It serves as a final authority to verify if a planned drone mission is safe to execute by checking for conflicts in space and time  against other drones’ flight trajectories.

The system supports 4D conflict detection (3D space + time) and provides detailed conflict reports, simulation visualizations, and a scalable foundation for future enhancements.

---

## Features

* **Spatial & Temporal Conflict Detection**
  Checks for mission conflicts within a defined safety buffer distance and overlapping time windows.

* **4D Mission Representation**
  Waypoints include x, y, and optional altitude (z), with timestamps for precise spatiotemporal analysis.

* **Conflict Explanation**
  Returns detailed info on conflict locations, times, and involved missions.

* **Simulation & Visualization**
  Visual graphs depict drone trajectories and highlight conflict zones dynamically.

* **Modular Design**
  Clean separation of core functionalities: mission models, conflict checking, I/O utilities, and visualization.

* **Demo Scripts**
  Simple runnable demos to illustrate conflict and no-conflict scenarios.

---

## Repository Structure

```
├── deconfliction_system/
│   ├── __init__.py
│   ├── models.py              # Mission and waypoint data models
│   ├── conflict_checker.py   # Core conflict detection logic
│   ├── io_utils.py           # Input/output and data parsing utilities
│   ├── visualization.py      # Plotting and animation utilities
│   └── checks.py             # (Optional) Additional checks or helper functions
│
│
├── main.py                       # Entry point to run the system interactively or extend functionality
│
└── README.md
```

---

## Setup Instructions

### Requirements

* Python 3.8+
* Packages:

  * numpy
  * matplotlib
  * scipy

### Running the system
Run in terminal: 
```
python3 -m main

```

## Design Decisions & Architectural Notes

* **4D Mission Model:** Missions are defined by waypoints with spatial coordinates plus timestamps for temporal accuracy.
* **Sampling-based Conflict Detection:** Positions interpolated at discrete time steps to efficiently approximate potential conflicts.
* **Safety Buffer:** A configurable distance threshold ensures minimum separation between drones.
* **Modularity:** Separation into data models, core logic, IO helpers, and visualization for maintainability and scalability.
* **Visualization:** Plots provide intuitive insight into spatiotemporal interactions, crucial for debugging and presentation.
* **Scalability:** Current system is single-threaded and ideal for dozens of drones; future versions should leverage distributed processing and real-time data pipelines for large-scale commercial operations.

---

## AI-Assisted Development

AI tools (including ChatGPT Plus and code generation assistants) were employed to:

* Accelerate boilerplate and algorithm development.
* Refine conflict checking logic and data modeling.
* Generate simulation code and visualization scripts.
* Assist with documentation and code comments.

All AI outputs were carefully reviewed, adapted, and tested to maintain correctness and project standards.

---

## Scaling to Real-World Operations

To scale for tens of thousands of commercial drones, the architecture must evolve:

* **Distributed Conflict Checking:** Partition airspace and missions, using distributed computation nodes.
* **Real-Time Data Ingestion:** Streaming drone telemetry integrated with conflict system.
* **Fault Tolerance & Resilience:** Redundant systems and fail-safe conflict resolution.
* **Efficient Spatial Indexing:** Use spatial data structures (e.g., KD-trees, R-trees) to reduce collision checks.
* **Incremental Updates:** Handle dynamic mission changes and incremental conflict recalculations.

---

## Future Enhancements

* Integrate with live UAV telemetry feeds.
* Add predictive AI to proactively adjust missions.
* Develop full 4D visualization (animated 3D + time).
* Expand conflict resolution strategies (rerouting, priority scheduling).
* Cloud-based deployment for scalable airspace management.

---

## Contact & Contribution

Developed by **Rithwiq Sunil Nair**, Aerial Robotics Engineer.

Contributions and feedback are welcome—please submit issues or pull requests.

---
