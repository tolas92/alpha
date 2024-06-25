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
import time


class AiCommand(Node):

    def __init__(self):
        super().__init__('AiCommand')
        self.command_ = self.create_subscription(String, '/table_number',self.callback, 10)
        self.navigator = BasicNavigator()
        self.counter=0

    def callback(self,msg): 
        while self.counter <10:
            #first go to table 1.
            goal_pose = PoseStamped()
            goal_pose.header.frame_id = 'map'
            goal_pose.header.stamp = self.navigator.get_clock().now().to_msg()
            goal_pose.pose.position.x =4.4
            goal_pose.pose.position.y =2.0
            goal_pose.pose.orientation.z=0.704
            goal_pose.pose.orientation.w = 0.710
            self.navigator.goToPose(goal_pose)
            while not self.navigator.isTaskComplete():
                feedback = self.navigator.getFeedback()
                feedback_=GoTo.Feedback()
                feedback_.distance_left=Duration.from_msg(feedback.estimated_time_remaining).nanoseconds / 1e9
            result = self.navigator.getResult() 
            self.navigator.clearGlobalCostmap()   
            time.sleep(10)
            goal_pose.header.stamp = self.navigator.get_clock().now().to_msg()
            goal_pose.pose.position.x =4.4
            goal_pose.pose.position.y =-1.0
            goal_pose.pose.orientation.z=-0.704
            goal_pose.pose.orientation.w = 0.710
            self.navigator.goToPose(goal_pose)
            while not self.navigator.isTaskComplete():
                feedback = self.navigator.getFeedback()
                feedback_=GoTo.Feedback()
                feedback_.distance_left=Duration.from_msg(feedback.estimated_time_remaining).nanoseconds / 1e9
            result = self.navigator.getResult()    
            self.navigator.clearGlobalCostmap()   

            time.sleep(10)
            goal_pose.header.stamp = self.navigator.get_clock().now().to_msg()
            goal_pose.pose.position.x =0.01
            goal_pose.pose.position.y =-0.01
            goal_pose.pose.orientation.z=0.0
            goal_pose.pose.orientation.w = 0.99
            self.navigator.goToPose(goal_pose)
            while not self.navigator.isTaskComplete():
                feedback = self.navigator.getFeedback()
                feedback_=GoTo.Feedback()
                feedback_.distance_left=Duration.from_msg(feedback.estimated_time_remaining).nanoseconds / 1e9
            result = self.navigator.getResult()    
            self.navigator.clearGlobalCostmap()   
            time.sleep(15)
            self.counter+=1

def main(args=None):
    rclpy.init(args=args)
    aicommand = AiCommand()
    rclpy.spin(aicommand)
    # If we press control + C, the node will stop.
    aicommand.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()