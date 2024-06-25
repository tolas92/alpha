from ollama import chat
import json
from rclpy.node import Node
from std_msgs.msg import String
import rclpy
from prototype.action import GoTo,FoodMenu,AiCamera
from rclpy.action import ActionClient
from google.cloud import texttospeech
from pygame import mixer

mixer.init()


class MasterAi(Node):    

    def __init__(self):
        super().__init__("masterAi_Node")
        self.timer=self.create_timer(1,self.local_ai_master)
        self.robot_publisher=self.create_publisher(String,'/move_robot',10)
        self.image_publisher=self.create_publisher(String,'/explain_image',10)
        self.file_opener=self.create_publisher(String,'/file_opener',10)
        self._action_client = ActionClient(self,AiCamera, '/AiCamera')
        self.ai_voice=''
        self.client = texttospeech.TextToSpeechClient()


    def robot_move(self,loc):
        msg=String()
        msg.data=loc
        self.robot_publisher.publish(msg)
        print("moving")
    
    def send_text(self,user_input):
        msg=String()
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
        #print(self.ai_reply)
        #print(self.ai_voice)
        """
        synthesis_input = texttospeech.SynthesisInput(text=self.ai_voice)

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.VoiceSelectionParams(
            language_code="hi-IN", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
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
        with open("output.wav", "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print('Audio content written to file "output.wav"')
            mixer.music.load('/home/tolasing/main_ws/ml_ws/output.wav')
            mixer.music.set_volume(10)
            mixer.music.play()
            while mixer.music.get_busy():
                pass
        """
        self.ai_voice=''
        

    def feedback_callback(self,feedback_msg):
        feedback=feedback_msg.feedback.ai_response
        self.ai_voice+=feedback+''
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
