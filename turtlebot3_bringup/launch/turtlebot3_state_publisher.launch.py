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

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import  Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution, FindPackageShare
from launch_ros.actions import Node


def generate_launch_description():
    TURTLEBOT3_MODEL = os.environ['TURTLEBOT3_MODEL']

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    prefix = LaunchConfiguration("prefix", default_value='""')
    urdf_file_name = 'turtlebot3_' + TURTLEBOT3_MODEL + '.urdf.xacro'

    print("urdf_file_name : {}".format(urdf_file_name))

# Get URDF via xacro
    robot_desc = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [FindPackageShare("turtlebot3_description"), "urdf", urdf_file_name]
            ),
            " ",
            "prefix:=",
            prefix,
        ]
    )
    rsp_params = {'robot_description': robot_desc}

    # print (robot_desc) # Printing urdf information.

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[rsp_params, {'use_sim_time': use_sim_time}])
    ])
