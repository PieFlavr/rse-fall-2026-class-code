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

```bash
# turtlebot nav2 thingy
source /opt/ros/jazzy/setup.bash
ros2 launch nav2_bringup tb3_simulation_launch.py headless:=False
```
