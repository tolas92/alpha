import time
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
import py_trees_ros_interfaces.action as py_trees_actions



class CoActionServer(Node):

    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
        py_trees_actions.Dock,
            '/dock',
            self.execute_callback)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        goal=goal_handle.request
    
        feedback_msg=py_trees_actions.Dock.Feedback()
        for i in range(1, 11):  # Loop for 10 seconds
            feedback_msg.percentage_completed = float(i)  # Update x-coordinate
            self.get_logger().info(f'Feedback: x={feedback_msg.percentage_completed}')
            goal_handle.publish_feedback(feedback_msg)         
            time.sleep(1)

        goal_handle.succeed()
        result = py_trees_actions.Dock.Result()
        result.message='ok'
        return result


def main(args=None):
    rclpy.init(args=args)

    fibonacci_action_server = CoActionServer()

    rclpy.spin(fibonacci_action_server)


if __name__ == '__main__':
    main()