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
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```
