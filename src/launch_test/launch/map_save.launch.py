
#!/usr/bin/env python3

# This is the launch file used for ROS Foxy and older. 
# Launch this file to save a map created in RViz.
# 建图完成后，还需输入命令：
# ros2 service call /map_saver/save_map nav2_msgs/srv/SaveMap "{map_topic: map, map_url: my_map, image_format: pgm, map_mode: trinary, free_thresh: 0.25, occupied_thresh: 0.65}"



import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

def generate_launch_description():

    # .................. Configurable Arguments .....................

    use_sim_time = True
    map_saver_params_file = 'map_saver_params.yaml'
    # ...............................................................


    pkg_dir = get_package_share_directory('launch_test')
    map_save_config = os.path.join(pkg_dir, 'params', map_saver_params_file)


    return LaunchDescription([

        DeclareLaunchArgument("use_sim_time", default_value=str(use_sim_time), description="Use simulation/Gazebo clock"),
        DeclareLaunchArgument("map_saver_params_file", default_value=map_save_config, description="Map Saver Configuration File"),

        Node(
            package='nav2_map_server',
            executable='map_saver_server',
            output='screen',
            emulate_tty=True,  
            parameters=[LaunchConfiguration('map_saver_params_file')]                  
        ),

        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager',
            output='screen',
            emulate_tty=True,  
            parameters=[
                {'use_sim_time': LaunchConfiguration('use_sim_time')},
                {'autostart': True},
                {'node_names': ['map_saver']}]
        )

    ])
