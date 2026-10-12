# RSE Nav2 Office Bringup

This package launches the `rse_office` Gazebo environment with a small Nav2 stack configured for the classroom robot.

## Install dependencies

```bash
sudo apt update
sudo apt install ros-jazzy-navigation2 ros-jazzy-nav2-bringup
```

From the workspace root:

```bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --packages-select rse_gazebo rse_nav2
source install/setup.bash
```

## Launch

```bash
ros2 launch rse_nav2 office_nav.launch.py
```

The default launch starts Gazebo, loads the office map, initializes AMCL at the robot's spawn pose, activates Nav2, and opens RViz.

Use **Nav2 Goal** in RViz to send a goal in the `map` frame.

The same conference-room goal can be sent from a terminal:

```bash
ros2 action send_goal \
  /navigate_to_pose nav2_msgs/action/NavigateToPose \
  "{pose: {header: {frame_id: map}, pose: {position: {x: 0.0, y: 2.6, z: 0.0}, orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}}}}" \
  --feedback
```

## Inspect the system

```bash
ros2 action list
ros2 action info /navigate_to_pose
ros2 lifecycle nodes
ros2 run tf2_ros tf2_echo map odom
ros2 topic echo /amcl_pose --once
```

## Practice manual localization

Disable the predefined AMCL pose:

```bash
ros2 launch rse_nav2 office_nav.launch.py set_initial_pose:=false
```

Then use **2D Pose Estimate** in RViz before sending a navigation goal.

## Launch Nav2 without restarting Gazebo

If the office simulation is already running:

```bash
ros2 launch rse_nav2 office_nav.launch.py gazebo:=false
```

## ROS 1 terminology

ROS 1 used the `move_base` action. Nav2 exposes the equivalent navigation behavior through the `nav2_msgs/action/NavigateToPose` action at `/navigate_to_pose`.
