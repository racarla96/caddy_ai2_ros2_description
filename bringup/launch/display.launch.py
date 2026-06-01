# Copyright (c) 2025 Rafael Carbonell Lázaro (racarla96)
# Licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0)
# See: https://creativecommons.org/licenses/by/4.0/

import os

import yaml
from ament_index_python.packages import get_package_share_directory
from jinja2 import Environment, FileSystemLoader

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration, OrSubstitution
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('namespace', default_value='',
                              description='ROS namespace for the robot'),
        DeclareLaunchArgument('prefix',    default_value='',
                              description='Link/joint name prefix (e.g. robot1_)'),
        DeclareLaunchArgument('simulation', default_value='false',
                              description='Joint states come from Gazebo simulation'),
        DeclareLaunchArgument('real_robot', default_value='false',
                              description='Joint states come from the real robot hardware'),
        DeclareLaunchArgument('use_rviz', default_value='true',
                              description='Launch RViz'),
        OpaqueFunction(function=_launch_display),
    ])


def _launch_display(context, *args, **kwargs):
    namespace = context.launch_configurations['namespace']
    prefix    = context.launch_configurations['prefix']

    desc_share = get_package_share_directory('caddy_ai2_ros2_description')

    with open(os.path.join(desc_share, 'bringup', 'config', 'robot_params.yaml')) as f:
        robot_params = yaml.safe_load(f)

    # --- Render URDF sensor fragments (link + visual + joint per enabled sensor) ---
    urdf_sensor_fragments = []
    for sensor_name, sensor_cfg in robot_params.get('sensors', {}).items():
        if not sensor_cfg.get('enabled', True):
            continue
        s_share = get_package_share_directory(sensor_cfg['package'])
        urdf_tpl = os.path.join(s_share, 'description', 'sensor.urdf.j2')
        if not os.path.isfile(urdf_tpl):
            continue
        pose = sensor_cfg['pose']
        s_env = Environment(
            loader=FileSystemLoader(os.path.join(s_share, 'description')),
            keep_trailing_newline=True,
        )
        urdf_sensor_fragments.append(s_env.get_template('sensor.urdf.j2').render(
            prefix=prefix,
            sensor_name=sensor_name,
            frame_id=sensor_cfg['frame_id'],
            x=pose['x'], y=pose['y'], z=pose['z'],
            roll=pose['roll'], pitch=pose['pitch'], yaw=pose['yaw'],
            sensor_share=s_share,
        ))

    urdf_dir = os.path.join(desc_share, 'description', 'model', 'urdf')
    env = Environment(loader=FileSystemLoader(urdf_dir), keep_trailing_newline=True)
    robot_description_str = env.get_template('caddy_ai2_model.urdf.j2').render(
        namespace=namespace,
        prefix=prefix,
        desc_share=desc_share,
        sensors_urdf_fragment='\n'.join(urdf_sensor_fragments),
        **robot_params,
    )

    simulation = context.launch_configurations.get('simulation', 'false').lower() == 'true'
    real_robot  = context.launch_configurations.get('real_robot',  'false').lower() == 'true'

    # In simulation/real-robot mode a joint_state_broadcaster already publishes /joint_states
    # and a robot_state_publisher already handles TF — suppress duplicate TF output here.
    tf_remaps = (
        [('tf', 'tf_rviz_unused'), ('tf_static', 'tf_static_rviz_unused')]
        if (simulation or real_robot) else []
    )

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher_rviz',
        namespace=namespace,
        output='screen',
        parameters=[{'robot_description': robot_description_str}],
        remappings=[('robot_description', 'robot_description_rviz')] + tf_remaps,
    )

    # Pass robot_description as parameter so joint_state_publisher can determine
    # which joints to publish regardless of the remapped topic name.
    node_joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        namespace=namespace,
        output='screen',
        parameters=[{'robot_description': robot_description_str}],
        condition=UnlessCondition(
            OrSubstitution(
                LaunchConfiguration('simulation'),
                LaunchConfiguration('real_robot'),
            )
        ),
    )

    node_rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=[
            '-d', os.path.join(desc_share, 'bringup', 'rviz', 'display.rviz'),
        ],
        condition=IfCondition(LaunchConfiguration('use_rviz')),
    )

    return [
        node_robot_state_publisher,
        node_joint_state_publisher,
        node_rviz2,
    ]
