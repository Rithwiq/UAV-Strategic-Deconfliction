from datetime import datetime, timedelta
from deconfliction_system.models import Waypoint, PrimaryMission
from deconfliction_system.conflict_checker import check_conflicts
from deconfliction_system.visualization import interactive_visualize_smooth_3d

def create_sample_missions():
    now = datetime.now()

    missions = []

    # Flight 1
    wps1 = [Waypoint(0, 0, 0), Waypoint(10, 10, 5), Waypoint(20, 5, 10)]
    m1 = PrimaryMission(
        name="Flight_One",
        waypoints=wps1,
        start_time=now,
        end_time=now + timedelta(minutes=15)
    )
    missions.append(m1)

    # Flight 2
    wps2 = [Waypoint(5, -5, 2), Waypoint(15, 15, 8), Waypoint(25, 10, 12)]
    m2 = PrimaryMission(
        name="Flight_Two",
        waypoints=wps2,
        start_time=now + timedelta(minutes=5),
        end_time=now + timedelta(minutes=20)
    )
    missions.append(m2)

    # Flight 3
    wps3 = [Waypoint(-10, 0, 3), Waypoint(0, 10, 6), Waypoint(10, 20, 9)]
    m3 = PrimaryMission(
        name="Flight_Three",
        waypoints=wps3,
        start_time=now - timedelta(minutes=10),
        end_time=now + timedelta(minutes=5)
    )
    missions.append(m3)

    # Flight 4
    wps4 = [Waypoint(0, 0, 0), Waypoint(5, 5, 7), Waypoint(15, 15, 7)]
    m4 = PrimaryMission(
        name="Flight_Four",
        waypoints=wps4,
        start_time=now + timedelta(minutes=2),
        end_time=now + timedelta(minutes=18)
    )
    missions.append(m4)

    return missions

def get_waypoint_from_input(index):
    while True:
        try:
            raw = input(f"Waypoint {index+1} (format: x y [z optional]): ").strip()
            parts = raw.split()
            if len(parts) < 2:
                raise ValueError("At least x and y required.")
            x, y = float(parts[0]), float(parts[1])
            z = float(parts[2]) if len(parts) > 2 else 0.0
            return Waypoint(x, y, z)
        except Exception:
            print("Invalid input, try again (example: 10 20 5)")

def get_mission_from_input():
    while True:
        try:
            name = input("Enter mission name: ").strip()
            start_str = input("Enter start time (YYYY-MM-DD HH:MM:SS): ").strip()
            end_str = input("Enter end time (YYYY-MM-DD HH:MM:SS): ").strip()
            start_time = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
            end_time = datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")
            if end_time <= start_time:
                print("End time must be after start time. Try again.")
                continue

            num_wp = int(input("Enter number of waypoints (>=2): ").strip())
            if num_wp < 2:
                print("Must have at least 2 waypoints. Try again.")
                continue

            waypoints = [get_waypoint_from_input(i) for i in range(num_wp)]

            return PrimaryMission(name=name, waypoints=waypoints, start_time=start_time, end_time=end_time)
        except Exception as e:
            print(f"Input error: {e}. Please try again.")

def main():
    print("=== Existing sample missions loaded ===")
    existing_missions = create_sample_missions()
    print(f"Loaded {len(existing_missions)} existing missions to check against.\n")

    print("=== Enter your primary mission details ===")
    user_mission = get_mission_from_input()

    print("\n=== Running conflict check... ===")
    conflicts = check_conflicts(user_mission, existing_missions)
    if conflicts:
        print(f"Conflicts detected with {len(conflicts)} mission(s):")
    for mission_name, points in conflicts.items():
        print(f" - {mission_name} | Conflict points: {points}")

    else:
        print("No conflicts detected. Flight plan is clear.")

        print("\n=== Launching interactive 3D visualization ===")
    interactive_visualize_smooth_3d(user_mission, existing_missions)

if __name__ == "__main__":
    main()
