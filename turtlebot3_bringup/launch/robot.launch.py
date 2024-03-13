#!/usr/bin/env python3
#
# Copyright 2019 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors: Darby Lim

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import ThisLaunchFileDir
from launch_ros.actions import Node
from launch.conditions import IfCondition

def generate_launch_description():
    TURTLEBOT3_MODEL = os.environ['TURTLEBOT3_MODEL']
    LDS_MODEL = os.environ['LDS_MODEL']
    LDS_LAUNCH_FILE = '/hlds_laser.launch.py'
    LDS_LAUNCH_ARGS = {'port': '/dev/ttyUSB0', 'frame_id': 'base_scan'} 

    usb_port = LaunchConfiguration('usb_port', default='/dev/ttyACM0')

    camera_params = LaunchConfiguration(
        'camera_params',
        default=os.path.join(
            get_package_share_directory('turtlebot3_bringup'),
            'param',
            'v4l2_camera.yaml'))

    tb3_params = LaunchConfiguration(
        'tb3_params',
        default=os.path.join(
            get_package_share_directory('turtlebot3_bringup'),
            'param',
            TURTLEBOT3_MODEL + '.yaml'))

    if LDS_MODEL == 'LDS-01':
        lidar_pkg_dir = LaunchConfiguration(
            'lidar_pkg_dir',
            default=os.path.join(get_package_share_directory('hls_lfcd_lds_driver'), 'launch'))
    elif LDS_MODEL == 'LDS-02':
        lidar_pkg_dir = LaunchConfiguration(
            'lidar_pkg_dir',
            default=os.path.join(get_package_share_directory('ld08_driver'), 'launch'))
        LDS_LAUNCH_FILE = '/ld08.launch.py'
    elif LDS_MODEL == 'YDLIDAR-G4':
        lidar_pkg_dir = LaunchConfiguration(
            'lidar_pkg_dir',
            default=os.path.join(get_package_share_directory('ydlidar_ros2_driver'), 'launch'))
        LDS_LAUNCH_FILE = '/ydlidar_launch.py'
        LDS_LAUNCH_ARGS = {'params_file': os.path.join(get_package_share_directory('turtlebot3_bringup'), 'param', 'ydlidar.yaml')}
    else:
        lidar_pkg_dir = LaunchConfiguration(
            'lidar_pkg_dir',
            default=os.path.join(get_package_share_directory('hls_lfcd_lds_driver'), 'launch'))
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    use_camera = LaunchConfiguration('use_camera', default='true')
    use_joystick = LaunchConfiguration('use_joystick', default='true')
   
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value=use_sim_time,
            description='Use simulation (Gazebo) clock if true'),

        DeclareLaunchArgument(
            'use_camera',
            default_value=use_camera,
            description='Use camera if true'),

        DeclareLaunchArgument(
            'use_joystick',
            default_value=use_joystick,
            description='Use joystick if true'),

        DeclareLaunchArgument(
            'usb_port',
            default_value=usb_port,
            description='Connected USB port with OpenCR'),

        DeclareLaunchArgument(
            'tb3_params',
            default_value=tb3_params,
            description='Full path to turtlebot3 parameter file to load'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [ThisLaunchFileDir(), '/turtlebot3_state_publisher.launch.py']),
            launch_arguments={'use_sim_time': use_sim_time}.items(),
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [ThisLaunchFileDir(), '/joystick.launch.py']),
            launch_arguments={'use_sim_time': use_sim_time}.items(),
            condition=IfCondition(use_joystick),
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([lidar_pkg_dir, LDS_LAUNCH_FILE]),
            launch_arguments=LDS_LAUNCH_ARGS.items(),
        ),

        Node(
            condition=IfCondition(use_camera),
            package='v4l2_camera',
            executable='v4l2_camera_node',
            parameters=[camera_params],
            output='screen'),

        Node(
            package='turtlebot3_node',
            executable='turtlebot3_ros',
            parameters=[tb3_params],
            arguments=['-i', usb_port],
            output='screen'),
    ])
