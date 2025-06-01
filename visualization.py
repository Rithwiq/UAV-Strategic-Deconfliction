import numpy as np
from plotly.graph_objs import Scatter3d, Figure
from datetime import timedelta
from scipy.interpolate import CubicSpline

def interactive_visualize_smooth_3d(primary_mission, other_missions=None):
    """
    Visualize primary mission and other missions in 3D with smooth spline interpolation.
    
    Args:
        primary_mission: Primary mission object with waypoints and start/end times.
        other_missions: List of other mission objects to plot alongside.
    """
    fig = Figure()

    def plot_mission(mission, color, line_width, marker_size, name):
        xs = [wp.x for wp in mission.waypoints]
        ys = [wp.y for wp in mission.waypoints]
        zs = [wp.z for wp in mission.waypoints]

        start = mission.start_time
        end = mission.end_time
        duration_seconds = (end - start).total_seconds()

        # Handle cases with 1 or 2 waypoints gracefully
        if len(xs) < 3:
            # Linear interpolation fallback
            interp_xs = np.linspace(xs[0], xs[-1], 300)
            interp_ys = np.linspace(ys[0], ys[-1], 300)
            interp_zs = np.linspace(zs[0], zs[-1], 300)
        else:
            waypoint_times = np.linspace(0, duration_seconds, len(xs))
            cs_x = CubicSpline(waypoint_times, xs)
            cs_y = CubicSpline(waypoint_times, ys)
            cs_z = CubicSpline(waypoint_times, zs)

            smooth_times = np.linspace(0, duration_seconds, 300)
            interp_xs = cs_x(smooth_times)
            interp_ys = cs_y(smooth_times)
            interp_zs = cs_z(smooth_times)

        # Plot waypoints
        fig.add_trace(Scatter3d(
            x=xs, y=ys, z=zs,
            mode='markers',
            marker=dict(size=marker_size, color=color),
            name=f"{name} Waypoints"
        ))

        # Plot smooth path
        fig.add_trace(Scatter3d(
            x=interp_xs, y=interp_ys, z=interp_zs,
            mode='lines',
            line=dict(color=color, width=line_width),
            name=f"{name} Path"
        ))

    # Plot primary mission in bold red-green colors
    plot_mission(primary_mission, color='green', line_width=5, marker_size=7, name=primary_mission.name)

    # Plot other missions in lighter colors
    if other_missions:
        for mission in other_missions:
            plot_mission(mission, color='blue', line_width=2, marker_size=4, name=mission.name)

    fig.update_layout(
        title='3D Mission Visualization: Primary vs Others',
        scene=dict(
            xaxis_title='X (meters)',
            yaxis_title='Y (meters)',
            zaxis_title='Z (meters)'
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        legend=dict(itemsizing='constant')
    )

    fig.show()
