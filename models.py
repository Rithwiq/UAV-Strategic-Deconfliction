from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, timedelta
import numpy as np

@dataclass
class Waypoint:
    x: float
    y: float
    z: float = 0.0  # Default altitude for 2D missions
    t: Optional[datetime] = None  # Timestamp in mission time (datetime)

@dataclass
class Mission:
    name: str
    waypoints: List[Waypoint]
    start_time: datetime
    end_time: datetime

    def interpolate(self, resolution: int = 100) -> List[Waypoint]:
        """Interpolate between waypoints spatially and assign interpolated timestamps."""
        if len(self.waypoints) < 2:
            return self.waypoints

        coords = np.array([[wp.x, wp.y, wp.z] for wp in self.waypoints])
        dists = np.sqrt(np.sum(np.diff(coords, axis=0)**2, axis=1))
        total_dist = np.insert(np.cumsum(dists), 0, 0)
        total_length = total_dist[-1]

        interp_points = np.linspace(0, total_length, resolution)
        interp_x = np.interp(interp_points, total_dist, coords[:, 0])
        interp_y = np.interp(interp_points, total_dist, coords[:, 1])
        interp_z = np.interp(interp_points, total_dist, coords[:, 2])

        duration_sec = (self.end_time - self.start_time).total_seconds()
        interp_times = [self.start_time + timedelta(seconds=t) for t in np.linspace(0, duration_sec, resolution)]

        return [
            Waypoint(x, y, z, t)
            for x, y, z, t in zip(interp_x, interp_y, interp_z, interp_times)
        ]

@dataclass
class PrimaryMission(Mission):
    def __post_init__(self):
        if not self.waypoints:
            return

        # Assign times to waypoints if missing
        if any(wp.t is None for wp in self.waypoints):
            if self.start_time is None or self.end_time is None:
                raise ValueError("start_time and end_time must be set if waypoint times are missing.")

            duration = (self.end_time - self.start_time).total_seconds()
            n = len(self.waypoints)
            for i, wp in enumerate(self.waypoints):
                wp.t = self.start_time + timedelta(seconds=(duration * i) / (n - 1))

    def get_position_at(self, query_time: datetime) -> tuple[float, float, float]:
        """
        Returns interpolated (x, y, z) position at a given datetime.
        Linear interpolation between waypoints based on time.
        """
        if query_time <= self.waypoints[0].t:
            wp = self.waypoints[0]
            return (wp.x, wp.y, wp.z)
        if query_time >= self.waypoints[-1].t:
            wp = self.waypoints[-1]
            return (wp.x, wp.y, wp.z)

        # Find two waypoints between which query_time falls
        for i in range(len(self.waypoints) - 1):
            wp_start = self.waypoints[i]
            wp_end = self.waypoints[i + 1]
            if wp_start.t <= query_time <= wp_end.t:
                total_seconds = (wp_end.t - wp_start.t).total_seconds()
                if total_seconds == 0:
                    return (wp_start.x, wp_start.y, wp_start.z)

                elapsed = (query_time - wp_start.t).total_seconds()
                ratio = elapsed / total_seconds
                x = wp_start.x + ratio * (wp_end.x - wp_start.x)
                y = wp_start.y + ratio * (wp_end.y - wp_start.y)
                z = wp_start.z + ratio * (wp_end.z - wp_start.z)
                return (x, y, z)

        # If no matching interval found (should not happen), return last waypoint
        wp = self.waypoints[-1]
        return (wp.x, wp.y, wp.z)

@dataclass
class SimulatedFlight(Mission):
    drone_id: Optional[str] = "SimDrone-001"

    def __post_init__(self):
        if not self.waypoints:
            return

        if any(wp.t is None for wp in self.waypoints):
            if self.start_time is None or self.end_time is None:
                raise ValueError("start_time and end_time must be set if waypoint times are missing.")

            duration = (self.end_time - self.start_time).total_seconds()
            n = len(self.waypoints)
            for i, wp in enumerate(self.waypoints):
                wp.t = self.start_time + timedelta(seconds=(duration * i) / (n - 1))

    def get_position_at(self, query_time: datetime) -> tuple[float, float, float]:
        # Same logic as PrimaryMission for position interpolation
        if query_time <= self.waypoints[0].t:
            wp = self.waypoints[0]
            return (wp.x, wp.y, wp.z)
        if query_time >= self.waypoints[-1].t:
            wp = self.waypoints[-1]
            return (wp.x, wp.y, wp.z)

        for i in range(len(self.waypoints) - 1):
            wp_start = self.waypoints[i]
            wp_end = self.waypoints[i + 1]
            if wp_start.t <= query_time <= wp_end.t:
                total_seconds = (wp_end.t - wp_start.t).total_seconds()
                if total_seconds == 0:
                    return (wp_start.x, wp_start.y, wp_start.z)

                elapsed = (query_time - wp_start.t).total_seconds()
                ratio = elapsed / total_seconds
                x = wp_start.x + ratio * (wp_end.x - wp_start.x)
                y = wp_start.y + ratio * (wp_end.y - wp_start.y)
                z = wp_start.z + ratio * (wp_end.z - wp_start.z)
                return (x, y, z)

        wp = self.waypoints[-1]
        return (wp.x, wp.y, wp.z)

@dataclass
class DeconflictionScenario:
    primary_mission: PrimaryMission
    simulated_flights: List[SimulatedFlight] = field(default_factory=list)

    def all_positions_at(self, query_time: datetime) -> dict:
        """
        Returns positions of the primary mission and all simulated flights at a given time.
        """
        positions = {
            "primary": self.primary_mission.get_position_at(query_time)
        }
        for flight in self.simulated_flights:
            positions[flight.drone_id] = flight.get_position_at(query_time)
        return positions
