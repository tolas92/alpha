import rclpy
import time
from rclpy.action import ActionClient
from rclpy.node import Node

from prototype.action import GoTo,FoodMenu


class FibonacciActionClient(Node):

    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._action_client = ActionClient(self,FoodMenu, '/Kitchen')

    def send_goal(self, msg):
        goal_msg = FoodMenu.Goal()
        goal_msg.order="table_1"
        print("hello")
        self._action_client.wait_for_server()
        print('hi')
        
        self._action_client.send_goal_async(goal_msg,feedback_callback=self.feedback_callback)
        print("sent goal ")
    
    def feedback_callback(self,feedback_msg):
        feedback=feedback_msg.feedback
        self.get_logger().info(f'Feedback: x={feedback}')


def main(args=None):
    rclpy.init(args=args)

    action_client = FibonacciActionClient()

    action_client.send_goal([10.0,20.0])

    rclpy.spin(action_client)


if __name__ == '__main__':
    main()