import time
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from prototype.action import AiCamera
from ollama import chat
import ollama



class CoActionServer(Node):

    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            AiCamera,
            '/AiCamera',
            self.execute_callback)
        

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        goal=goal_handle.request.user_request
        feedback_msg=AiCamera.Feedback()
    
        stream = ollama.chat(
        model='orca-mini:3b',
        messages=[{'role': 'user', 'content': goal}],
        stream=True,
    )


        for chunk in stream:  # Loop for 10 seconds
        # feedback_msg.distance_left = float(i)  # Update x-coordinate 
            #self.get_logger().info(f'Feedback: x={i},')
            feedback_msg.ai_response=chunk['message']['content']
            goal_handle.publish_feedback(feedback_msg)         

        goal_handle.succeed()
        result = AiCamera.Result()
        result.ai_end="."
        return result
        #rclpy.shutdown()
        


def main(args=None):
    rclpy.init(args=args)

    fibonacci_action_server = CoActionServer()

    rclpy.spin(fibonacci_action_server)


if __name__ == '__main__':
    main()