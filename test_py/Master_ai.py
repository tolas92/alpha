import time
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from rclpy.action import ActionClient
import ollama

class MasterAi(Node):    

    def __init__(self):
        super().__init__("masterAi_Node")
        self.timer=self.create_timer(1,self.local_ai_master)
        self.robot_publisher=self.create_publisher(String,'/move_robot',10)
        self.image_publisher=self.create_publisher(String,'/explain_image',10)
        self.file_opener=self.create_publisher(String,'/file_opener',10)
        self._action_client = ActionClient(self,AiCamera, '/AiCamera')


    def robot_move(self,loc):
        msg=String()
        msg.data=loc
        self.robot_publisher.publish(msg)
        print("moving")
    
    def send_text(self,user_input):
        goal_msg=AiCamera.Goal()
        goal_msg.user_request=user_input
        self._action_client.wait_for_server()
        self._send_goal_future=self._action_client.send_goal_async(goal_msg,feedback_callback=self.feedback_callback)
        rclpy.spin_until_future_complete(self,self._send_goal_future)
        self.goal_handle=self._send_goal_future.result()
        if not self.goal_handle.accepted:
            print('rejected')
            return
        self.result_future=self.goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self,self.result_future)
        self.ai_reply=self.result_future.result().result.ai_end
        print(self.ai_reply)

    def feedback_callback(self,feedback_msg):
        feedback=feedback_msg.feedback.ai_response
        print(feedback, end='', flush=True)

        #self.get_logger().info(f'Feedback: x={feedback}')
        return
   

    def local_ai_master(self):
        self.timer.cancel()
        #self.send_text(1)


def main(args=None):
 rclpy.init(args=args)
 master_ai=MasterAi()
 while rclpy.ok():
    user_input = input("\033[94mYou:\033[0m")
    if user_input.lower() == "exit":
        print("Exiting...")
        break
    master_ai.send_text(user_input)
    rclpy.spin_once(master_ai)
        
 master_ai.destroy_node()
 rclpy.shutdown()

            
    
if __name__ == "__main__":
    main()
