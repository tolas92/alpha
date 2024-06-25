import time
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from prototype.action import AiCamera
from ollama import chat
import ollama
import subprocess
import tkinter as tk
import threading



class CoActionServer(Node):

    def __init__(self):
        super().__init__('ai_action_server')
        self._action_server = ActionServer(
            self,
            AiCamera,
            '/AiCamera',
            self.execute_callback)
        self.terminal_opened = False
        self.terminal_process = None
        self.open_terminal()

    def open_terminal(self):
        self.terminal_process = subprocess.Popen(["gnome-terminal", "--"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.terminal_opened = True

        


    def execute_callback(self, goal_handle):
        #self.get_logger().info('Executing goal...')
        goal=goal_handle.request.user_request
        self.msg_list.insert(tk.END, f"You: {goal}\n")
        feedback_msg=AiCamera.Feedback()
        stream = ollama.chat(
        model='MistCom:latest',
        messages=[{'role': 'user', 'content': f'Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\n### Instruction:\n{goal}\n### Input:\n\n### Response:'}],
        stream=True,
        )

        self.msg_list.insert(tk.END, f"Assitant:\n")
        for chunk in stream:  # Loop for 10 seconds
            feedback_msg.ai_response=chunk['message']['content']
            goal_handle.publish_feedback(feedback_msg)
            self.msg_list.insert(tk.END,chunk['message']['content']) 
            #print(chunk['message']['content'], end='',flush=True)
        #print()
            
        self.msg_list.insert(tk.END,'\n')
        goal_handle.succeed()
        result = AiCamera.Result()
        result.ai_end="."
        return result
        #rclpy.shutdown()

def run_ros_node(node):
    rclpy.spin(node)

def on_close(node, root):
    node.destroy_node()
    rclpy.shutdown()
    root.destroy()
    
    

def main(args=None):
    rclpy.init(args=args)

    ai_action_server = CoActionServer()

    rclpy.spin(ai_action_server)
     # Set up the GUI in the main thread
    root = tk.Tk()
    root.title("ROSIE")
    ai_action_server.msg_list = tk.Text(root, height=15, width=50)
    ai_action_server.msg_list.pack(padx=5, pady=5)
    ai_action_server.entry = tk.Entry(root)
    ai_action_server.entry.pack(padx=5, pady=5)
    ai_action_server.button = tk.Button(root, text="Send", command=ai_action_server.send_message)
    ai_action_server.button.pack(padx=5, pady=5)
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(ai_action_server, root))

    # Run the ROS node in a separate thread
    ros_thread = threading.Thread(target=run_ros_node, args=(ai_action_server,))
    ros_thread.start()

    # Start the Tkinter event loop in the main thread
    root.mainloop()


if __name__ == '__main__':
    main()
    

