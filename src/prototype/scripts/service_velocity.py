import rclpy
from std_srvs.srv import SetBool
from std_msgs.msg import Float64MultiArray
from rclpy.node import Node

class Service(Node):
      def __init__(self):
         super().__init__('service_velocity')
         self.service=self.create_service(SetBool,'shaft_velocity',self.SetBool_callback)

      def SetBool_callback(self,request,response):
          self.publisher_=self.create_publisher(Float64MultiArray,'velocity_controller/commands',10)
          command=Float64MultiArray()

          if request.data==True:
           command.data.append(2.0)
           self.publisher_.publish(command)
           self.get_logger().info('publising %s' %command)
           response.success=False
           response.message='rotating'

          if request.data==False:
           command.data.append(0.0)
           self.publisher_.publish(command)
           self.get_logger().info('publishing %s' %command)
           response.success=False
           response.message='stopping'
          return response    
def main(args=None):
    rclpy.init()
    rotating_service=Service()
    rclpy.spin(rotating_service)
    rclpy.shutdown()

if __name__=='__main__':
   main()


