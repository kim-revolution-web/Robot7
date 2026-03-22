cmake_minimum_required(VERSION 3.8)
project(team_pro_interface)

################################
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

####################################

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

################################################################################
# Find and load build settings from external packages
################################################################################
find_package(ament_cmake REQUIRED)
find_package(builtin_interfaces REQUIRED)
find_package(rosidl_default_generators REQUIRED)
################################################################################
# Declare ROS messages, services and actions
################################################################################
set(msg_files
  "msg/MsgFloat.msg"
)

# set(srv_files
#   "srv/?.srv"
# )

# set(action_files
#   "action/?.action"
# )

rosidl_generate_interfaces(${PROJECT_NAME}
  ${msg_files}
  # ${srv_files}
  # ${action_files}
  DEPENDENCIES builtin_interfaces
)

################################################################################
# Macro for ament package
################################################################################
ament_export_dependencies(rosidl_default_runtime)
ament_package()
