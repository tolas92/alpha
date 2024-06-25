#! /usr/bin/env python3

import time
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from prototype.action import AiCamera
from ollama import chat
import ollama
from google.cloud import texttospeech
from pygame import mixer
import logging
import tkinter as tk
import threading


#logging.basicConfig(level=logging.DEBUG)
try:
    mixer.init()
except Exception as e:
    logging.error(f"An error occurred while initializing the mixer: {e}")


class CoActionServer(Node):

    def __init__(self):
        super().__init__('ai_action_server')
        self._action_server = ActionServer(
            self,
            AiCamera,
            '/AiCamera',
            self.execute_callback)
        self.ai_voice=''
        self.client = texttospeech.TextToSpeechClient()   

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
        for chunk in stream:
            feedback_msg.ai_response=chunk['message']['content']
            self.ai_voice+=chunk['message']['content']+''
            goal_handle.publish_feedback(feedback_msg)     
            #print(chunk['message']['content'], end='',flush=True)
            self.msg_list.insert(tk.END,chunk['message']['content'])
           
        self.msg_list.insert(tk.END,'\n')
        synthesis_input = texttospeech.SynthesisInput(text=self.ai_voice)

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # The response's audio_content is binary.
        with open("/home/tolasing/main_ws/ml_ws/ai_server/scripts/output.wav", "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            mixer.music.load('/home/tolasing/main_ws/ml_ws/ai_server/scripts/output.wav')
            mixer.music.set_volume(10)
            mixer.music.play()
            while mixer.music.get_busy():
                pass


        goal_handle.succeed()

        result = AiCamera.Result()
        result.ai_end="."
        self.ai_voice=''
        return result
        #rclpy.shutdown()
    def send_message(self):
        print('ok')
    
def run_ros_node(node):
    rclpy.spin(node)

def on_close(node, root):
    node.destroy_node()
    rclpy.shutdown()
    root.destroy()
    

def main(args=None):
    rclpy.init(args=args)

    ai_action_server = CoActionServer()
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
    

