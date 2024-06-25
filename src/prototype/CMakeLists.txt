cmake_minimum_required(VERSION 3.8)
project(prototype)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(urdf REQUIRED)
find_package(xacro REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(rosidl_default_generators REQUIRED)

install(
  DIRECTORY
    config
    launch
    maps
    action
    worlds
    models
    urdf
    sambot
    meshes
    scripts
    rviz
    msg
  DESTINATION
    share/${PROJECT_NAME}/
)

install(
  PROGRAMS
  scripts/move_laser.py 
  scripts/move_shaft.py
  scripts/action_client.py
  DESTINATION lib/${PROJECT_NAME}
)

rosidl_generate_interfaces(${PROJECT_NAME}
  "action/SendCoordinates.action"
  "action/GoTo.action"
  "action/FoodMenu.action"
  "action/AiCamera.action"
  "msg/Food.msg"
  "msg/DistanceAngle.msg"
  DEPENDENCIES std_msgs
)



if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  #set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  #set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()