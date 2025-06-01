from datetime import timedelta
import math

def check_conflicts(primary_mission, other_missions, distance_threshold=10, time_step_seconds=5):
    """
    Checks for conflicts between the primary mission and other missions.

    Args:
        primary_mission: PrimaryMission object to check.
        other_missions: List of PrimaryMission objects.
        distance_threshold: Minimum safe distance (meters).
        time_step_seconds: Time step for sampling positions.

    Returns:
        Dict mapping conflicting mission names to lists of conflict details:
        {
            "mission_name": [
                {"time": datetime_obj, "location": (x, y, z)},
                ...
            ],
            ...
        }
        If no conflicts, returns an empty dict.
    """
    conflicts = {}
    
    primary_start = primary_mission.start_time
    primary_end = primary_mission.end_time

    for other in other_missions:
        # Skip self-comparison
        if other.name == primary_mission.name:
            continue

        # Check for time overlap
        latest_start = max(primary_start, other.start_time)
        earliest_end = min(primary_end, other.end_time)
        overlap_seconds = (earliest_end - latest_start).total_seconds()

        if overlap_seconds <= 0:
            continue  # No temporal overlap = no conflict

        # Time sampling at regular intervals
        time_points = [
            latest_start + timedelta(seconds=s)
            for s in range(0, int(overlap_seconds) + 1, time_step_seconds)
        ]

        conflict_points = []
        for t in time_points:
            p1 = primary_mission.get_position_at(t)
            p2 = other.get_position_at(t)

            if p1 is None or p2 is None:
                continue  # Outside mission range or undefined

            if euclidean_distance(p1, p2) < distance_threshold:
                conflict_points.append({"time": t, "location": p1})

        if conflict_points:
            conflicts[other.name] = conflict_points

    return conflicts


def euclidean_distance(p1, p2):
    """
    Calculates the 3D Euclidean distance between two points.
    Args:
        p1, p2: Tuples representing (x, y, z)
    Returns:
        float: distance in meters
    """
    return math.sqrt(
        (p1[0] - p2[0])**2 +
        (p1[1] - p2[1])**2 +
        (p1[2] - p2[2])**2
    )
