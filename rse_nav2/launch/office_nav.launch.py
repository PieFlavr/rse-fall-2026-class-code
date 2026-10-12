"""Launch the RSE office simulation with AMCL and a minimal Nav2 stack."""

from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, GroupAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    nav_share = Path(get_package_share_directory("rse_nav2"))
    gazebo_share = Path(get_package_share_directory("rse_gazebo"))
    nav2_bringup_share = Path(get_package_share_directory("nav2_bringup"))

    params_file = nav_share / "config" / "office_nav2.yaml"
    map_file = gazebo_share / "maps" / "rse_office.yaml"
    office_launch = gazebo_share / "launch" / "office.launch.py"
    rviz_config = nav2_bringup_share / "rviz" / "nav2_default_view.rviz"

    use_sim_time = LaunchConfiguration("use_sim_time")
    autostart = LaunchConfiguration("autostart")
    start_gazebo = LaunchConfiguration("gazebo")
    start_rviz = LaunchConfiguration("rviz")
    set_initial_pose = LaunchConfiguration("set_initial_pose")

    common_parameters = [
        str(params_file),
        {"use_sim_time": use_sim_time},
    ]

    gazebo = GroupAction(
        scoped=True,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(str(office_launch)),
                launch_arguments={
                    "use_sim_time": use_sim_time,
                    "rviz": "false",
                }.items(),
                condition=IfCondition(start_gazebo),
            )
        ],
    )

    map_server = Node(
        package="nav2_map_server",
        executable="map_server",
        name="map_server",
        output="screen",
        parameters=[
            str(params_file),
            {
                "use_sim_time": use_sim_time,
                "yaml_filename": str(map_file),
            },
        ],
    )

    amcl = Node(
        package="nav2_amcl",
        executable="amcl",
        name="amcl",
        output="screen",
        parameters=[
            str(params_file),
            {
                "use_sim_time": use_sim_time,
                "set_initial_pose": set_initial_pose,
            },
        ],
    )

    planner_server = Node(
        package="nav2_planner",
        executable="planner_server",
        name="planner_server",
        output="screen",
        parameters=common_parameters,
    )

    smoother_server = Node(
        package="nav2_smoother",
        executable="smoother_server",
        name="smoother_server",
        output="screen",
        parameters=common_parameters,
    )

    controller_server = Node(
        package="nav2_controller",
        executable="controller_server",
        name="controller_server",
        output="screen",
        parameters=common_parameters,
        remappings=[("cmd_vel", "/cmd_vel")],
    )

    behavior_server = Node(
        package="nav2_behaviors",
        executable="behavior_server",
        name="behavior_server",
        output="screen",
        parameters=common_parameters,
    )

    bt_navigator = Node(
        package="nav2_bt_navigator",
        executable="bt_navigator",
        name="bt_navigator",
        output="screen",
        parameters=common_parameters,
    )

    lifecycle_manager = Node(
        package="nav2_lifecycle_manager",
        executable="lifecycle_manager",
        name="lifecycle_manager_navigation",
        output="screen",
        parameters=[
            {
                "use_sim_time": use_sim_time,
                "autostart": autostart,
                "node_names": [
                    "map_server",
                    "amcl",
                    "planner_server",
                    "smoother_server",
                    "controller_server",
                    "behavior_server",
                    "bt_navigator",
                ],
            }
        ],
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", str(rviz_config)],
        parameters=[{"use_sim_time": use_sim_time}],
        condition=IfCondition(start_rviz),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="true",
                description="Use Gazebo simulation time.",
            ),
            DeclareLaunchArgument(
                "autostart",
                default_value="true",
                description="Configure and activate all lifecycle nodes.",
            ),
            DeclareLaunchArgument(
                "gazebo",
                default_value="true",
                description="Start the rse_office Gazebo simulation.",
            ),
            DeclareLaunchArgument(
                "rviz",
                default_value="true",
                description="Start RViz with the Nav2 default view.",
            ),
            DeclareLaunchArgument(
                "set_initial_pose",
                default_value="true",
                description="Initialize AMCL at the robot's Gazebo spawn pose.",
            ),
            gazebo,
            map_server,
            amcl,
            planner_server,
            smoother_server,
            controller_server,
            behavior_server,
            bt_navigator,
            lifecycle_manager,
            rviz,
        ]
    )
