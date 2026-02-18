# Copyright (c) 2025 Rafael Carbonell Lázaro (racarla96)
# Licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0)
# See: https://creativecommons.org/licenses/by/4.0/

cmake_minimum_required(VERSION 3.16)
project(caddy_ai2_ros2_description)

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)

install(
  DIRECTORY bringup description meshes
  DESTINATION share/${PROJECT_NAME}
)

ament_package()