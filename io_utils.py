import json
from datetime import datetime
from typing import List
from deconfliction_system.models import Waypoint, PrimaryMission, SimulatedFlight

def parse_waypoints(wps: List[dict]) -> List[Waypoint]:
    return [
        Waypoint(
            x=wp["x"],
            y=wp["y"],
            z=wp.get("z", 0),
            time=datetime.fromisoformat(wp["time"])
        )
        for wp in wps
    ]

def load_primary_mission(path: str) -> PrimaryMission:
    with open(path, "r") as f:
        data = json.load(f)
    return PrimaryMission(
        waypoints=parse_waypoints(data["waypoints"]),
        start_time=datetime.fromisoformat(data["start_time"]),
        end_time=datetime.fromisoformat(data["end_time"])
    )

def load_simulated_flights(path: str) -> List[SimulatedFlight]:
    with open(path, "r") as f:
        data = json.load(f)
    return [
        SimulatedFlight(
            drone_id=flight["drone_id"],
            waypoints=parse_waypoints(flight["waypoints"])
        )
        for flight in data["simulated_flights"]
    ]
