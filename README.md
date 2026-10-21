# Convenience Scripts

```bash
# With Building
export ROS_DOMAIN_ID=34
source /opt/ros/jazzy/setup.bash
cd ~/Desktop/Gemini-Repository/CPE491-class/rse_ws
colcon build --symlink-install
source install/setup.bash 
cd src/amanita
```

From the [documentation here](https://docs.nav2.org/jazzy/getting_started/quickstart/quickstart/), the following can be used:

```bash
# turtlebot nav2 thingy
export ROS_DOMAIN_ID=34
ros2 launch nav2_bringup tb3_simulation_launch.py headless:=False
```

```bash
# gazebo office launch
export ROS_DOMAIN_ID=34
ros2 launch rse_gazebo office.launch.py
```

```bash
# gazebo warehouse launch
export ROS_DOMAIN_ID=34
ros2 launch rse_gazebo waraehouse.launch.py
```

```bash
export ROS_DOMAIN_ID=34
ros2 launch rse_perception perception.launch.py
```
