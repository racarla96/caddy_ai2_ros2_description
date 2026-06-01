#!/usr/bin/env python3
"""
Render the Jinja2 URDF templates and write the result to stdout or a file.

Usage (after sourcing the workspace):
    ros2 run caddy_ai2_ros2_description render_urdf
    ros2 run caddy_ai2_ros2_description render_urdf -o /tmp/robot.urdf
"""

import argparse
import os
import sys

import yaml
from ament_index_python.packages import get_package_share_directory
from jinja2 import Environment, FileSystemLoader


def main():
    parser = argparse.ArgumentParser(description='Render the caddy_ai2 URDF templates.')
    parser.add_argument('--namespace', default='', help='ROS namespace')
    parser.add_argument('--prefix',    default='', help='Link/joint name prefix')
    parser.add_argument('-o', '--output', default=None, help='Output file (default: stdout)')
    args = parser.parse_args()

    desc_share = get_package_share_directory('caddy_ai2_ros2_description')

    with open(os.path.join(desc_share, 'bringup', 'config', 'robot_params.yaml')) as f:
        robot_params = yaml.safe_load(f)

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
            prefix=args.prefix,
            sensor_name=sensor_name,
            frame_id=sensor_cfg['frame_id'],
            x=pose['x'], y=pose['y'], z=pose['z'],
            roll=pose['roll'], pitch=pose['pitch'], yaw=pose['yaw'],
            sensor_share=s_share,
        ))

    urdf_dir = os.path.join(desc_share, 'description', 'model', 'urdf')
    env = Environment(loader=FileSystemLoader(urdf_dir), keep_trailing_newline=True)
    result = env.get_template('caddy_ai2_model.urdf.j2').render(
        namespace=args.namespace,
        prefix=args.prefix,
        desc_share=desc_share,
        sensors_urdf_fragment='\n'.join(urdf_sensor_fragments),
        **robot_params,
    )

    if args.output:
        with open(args.output, 'w') as f:
            f.write(result)
        print(f'Written to {args.output}', file=sys.stderr)
    else:
        print(result)


if __name__ == '__main__':
    main()
