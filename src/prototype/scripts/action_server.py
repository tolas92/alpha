import time
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from py_trees_ros_interfaces.action import Dock
from prototype.action import SendCoordinates,FoodMenu


class CoActionServer(Node):

    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            FoodMenu,
            '/Kitchen',
            self.execute_callback)
        

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        goal_handle.succeed()
        goal=goal_handle.request
        feedback_msg=FoodMenu.Feedback()
        for i in range(1, 11):  # Loop for 10 seconds
           # feedback_msg.distance_left = float(i)  # Update x-coordinate 
            self.get_logger().info(f'Feedback: x={i},')
            feedback_msg.waiting="waiting"
            goal_handle.publish_feedback(feedback_msg)         
            time.sleep(1)

        goal_handle.succeed()
        result = FoodMenu.Result()
        time.sleep(20)
        result.done=True
        return result


def main(args=None):
    rclpy.init(args=args)

    fibonacci_action_server = CoActionServer()

    rclpy.spin(fibonacci_action_server)


if __name__ == '__main__':
    main()