#!/usr/bin/python3

import rclpy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from rclpy.node import Node
#from gesture_recognition import *
#from cvfpscalc import CvFpsCalc
#from cv_bridge import CvBridge, CvBridgeError
#import cv2 as cv


class HandSignRecognition(Node):

    def __init__(self):
        # Creates a node with name 'hand_sign_recognition' and make sure it is a
        # unique node (using anonymous=True).
        super().__init__('hand_sign_recognition')
        self.subscription = self.create_subscription(Image,"/image_raw",self.callback,10)
        # Publisher which will publish to the topic 
        self.publisher_ =self.create_publisher(String,"/publish_gesture_topic",10)

        # Create a gesture recognition object that loads labels and train model
      #  self.gesture_detector = GestureRecognition("/home/tolasing/ai_ws/ros_hand_gesture_recognition/src/model/keypoint_classifier/keypoint_classifier_label.csv",
             #                                   "/home/tolasing/ai_ws/src/ros_hand_gesture_recognition/src/model/keypoint_classifier/keypoint_classifier.tflite")
       # self.bridge = CvBridge()
        #self.cv_fps_calc = CvFpsCalc(buffer_len=10)

    def callback(self, image_msg):
        """A callback function for the image subscriber

        Args:
            image_msg (sensor_msgs.msg): image message
        """
        #try:
         #   cv_image = self.bridge.imgmsg_to_cv2(image_msg)
          #  debug_image, gesture = self.gesture_detector.recognize(cv_image)
           # self.publisher_.publish(gesture)
            #if rospy.get_param("hand_sign_recognition/show_image"):
            #fps = self.cv_fps_calc.get()
            #debug_image = self.gesture_detector.draw_fps_info(debug_image, fps)
            #cv.imshow('ROS Gesture Recognition', debug_image)
            #cv.waitKey(10) # wait for 10 milisecond
        #except CvBridgeError as error:
            #print(error)
        print("hello")

def main(args=None):
    print("hello")
    rclpy.init(args=args)
    hand_sign = HandSignRecognition()
    rclpy.spin(hand_sign)
    # If we press control + C, the node will stop.
    hand_sign.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

