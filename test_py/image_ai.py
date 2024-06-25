from ollama import chat
import json
from rclpy.node import Node
from std_msgs.msg import String
import rclpy
from prototype.action import AiCamera
from rclpy.action import ActionServer
import time




class ImageAi(Node):    

    def __init__(self):
        super().__init__("masterAi_Node")
        self.timer=self.create_timer(1,self.local_ai_master)
        self.robot_publisher=self.create_publisher(String,'/move_robot',10)
        self.image_publisher=self.create_publisher(String,'/explain_image',10)
        self.file_opener=self.create_publisher(String,'/file_opener',10)
        self._action_server = ActionServer(self,AiCamera, '/AiCamera',self.execute_callback)


    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        goal=goal_handle.request
        feedback_msg=AiCamera.Feedback()
        for i in range(1, 2):  # Loop for 10 seconds
           # feedback_msg.distance_left = float(i)  # Update x-coordinate 
            self.get_logger().info(f'Feedback: x={i},')
            feedback_msg.waiting="waiting"
            goal_handle.publish_feedback(feedback_msg)         
            time.sleep(1)

        
        goal_handle.succeed()
        result = AiCamera.Result()
        result.response="this is ai "
        return result
    
    
    def robot_move(self,loc):
        msg=String()
        msg.data=loc
        self.robot_publisher.publish(msg)
        print("moving")
    
    def image_explain(self,camera_number):
        goal_msg=AiCamera.Goal()
        goal_msg.camera=camera_number
        self._action_client.wait_for_server()
        self._send_goal_future=self._action_client.send_goal_async(goal_msg,feedback_callback=self.feedback_callback)
        rclpy.spin_until_future_complete(self,self._send_goal_future)
        self.goal_handle=self._send_goal_future.result()
        if not self.goal_handle.accepted:
            print('rejected')
            return
        print('accpted')
        self.result_future=self.goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self,self.result_future)
        self.ai_reply=self.result_future.result().result.response
        return self.ai_reply

        
    def goal_response_callback(self,future):
        goal_handle=future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected:(')
            return
        self.get_logger().info("Goal accepted:)")
        self._get_result_future=goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self,future):
        result=future.result().result
        self.get_logger().info('Result: {0}'.format(result.response))
        return    
        
    def feedback_callback(self,feedback_msg):
        feedback=feedback_msg.feedback
        self.get_logger().info(f'Feedback: x={feedback}')
        return
   

    def local_ai_master(self):
     self.timer.cancel()
     while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Exiting...")
            break
        
        messages = [{'role': 'user', 'content': user_input}]
        response = chat('gorilla', messages=messages)
        
        assistant_response = response["message"]["content"]
        print("Assistant:",assistant_response)
        # Call the function if it's present in the assistant response
        try:
              eval(assistant_response)# Attempt to evaluate and execute the expression
        except Exception as e:
            print("Error executing assistant response:", e)




def main(args=None):
 rclpy.init(args=args)
 master_ai=MasterAi()
 rclpy.spin(master_ai)
 master_ai.destroy_node()
 rclpy.shutdown()

            
    
if __name__ == "__main__":
    main()
