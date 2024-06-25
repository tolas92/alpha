import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from prototype.action import AiCamera

class AiCameraActionServer(Node):

    def __init__(self):
        super().__init__('ai_camera_action_server')
        self._action_server = ActionServer(
            self,
            AiCamera,
            '/AiCamera',
            self.execute_callback
        )

    def execute_callback(self, goal_handle):
        self.get_logger().info(f'Received goal request: {goal_handle.request.user_request}')

        feedback_msg = AiCamera.Feedback()
        feedback_msg.ai_response = f'Received: {goal_handle.request.user_request}'
        
        # Publish feedback
        goal_handle.publish_feedback(feedback_msg)
        self.get_logger().info(f'Published feedback: {feedback_msg.ai_response}')

        # Simulate processing time
        rclpy.spin_once(self, timeout_sec=1)

        goal_handle.succeed()
        
        result = AiCamera.Result()
        result.ai_end = f'Processed: {goal_handle.request.user_request}'
        self.get_logger().info(f'Result: {result.ai_end}')
        return result

def main(args=None):
    rclpy.init(args=args)
    action_server = AiCameraActionServer()
    rclpy.spin(action_server)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
