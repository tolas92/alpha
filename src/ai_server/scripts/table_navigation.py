#! /usr/bin/env python3
# Copyright 2021 Samsung Research America
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

from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy
from std_msgs.msg import String
from rclpy.node import Node
from rclpy.duration import Duration
from rclpy.action import ActionServer ,GoalResponse,CancelResponse
from rclpy.action import GoalResponse
from prototype.action import GoTo


class AiCommand(Node):

    def __init__(self):
        super().__init__('AiCommand')
       # self.command_ = self.create_subscription(String, '/hand_gesture',self.callback, 10)
        self.action_server_=ActionServer(self,GoTo,'/table_nav',self.callback)
        self.navigator = BasicNavigator()

    def callback(self, goal_handle): 
        goal=goal_handle.request
        goal_pose = PoseStamped()
        goal_pose.header.frame_id = 'map'
        goal_pose.header.stamp = self.navigator.get_clock().now().to_msg()
        goal_pose.pose.position.x =goal.x
        goal_pose.pose.position.y =goal.y
        goal_pose.pose.orientation.z=goal.z
        goal_pose.pose.orientation.w = 1.0

    
        self.navigator.goToPose(goal_pose)
        
        
        while not self.navigator.isTaskComplete():
        
            feedback = self.navigator.getFeedback()
            feedback_=GoTo.Feedback()
            feedback_.distance_left=Duration.from_msg(feedback.estimated_time_remaining).nanoseconds / 1e9

            goal_handle.publish_feedback(feedback_)

            print('Estimated time of arrival: ' + '{0:.0f}'.format(
                   Duration.from_msg(feedback.estimated_time_remaining).nanoseconds / 1e9)
                    + ' seconds.')
        
        # Do something depending on the return code
        result = self.navigator.getResult()
        result_=GoTo.Result()
        """
        if result == TaskResult.SUCCEEDED:
            goal_handle.succeed()
            result_.done=True
            print('Goal succeeded!')
        elif result == TaskResult.CANCELED:
            goal_handle.canceled()
            result_.done=False
            print('Goal was canceled!')
        elif result == TaskResult.FAILED:
            goal_handle.abort()
            result_.done=False
            print('Goal failed!')
        else:
            print('Goal has an invalid return status!')
        
        return result_
        """
        goal_handle.succeed()
        result_.done=True
        return result_
        #self.navigator.lifecycleShutdown()
        
        #exit(0)

def main(args=None):
    rclpy.init(args=args)
    aicommand = AiCommand()
    rclpy.spin(aicommand)
    # If we press control + C, the node will stop.
    aicommand.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()