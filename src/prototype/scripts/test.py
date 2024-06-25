import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped, Point, Quaternion
from builtin_interfaces.msg import Time
import string
from prototype.msg import Food

class GoalSub(Node):
    def __init__(self):
        super().__init__('table_node')
        self.publisher = self.create_publisher(String, "/test", 10)
        self.timer = self.create_timer(1, self.on_timer)

    def on_timer(self):
        msg=String()
        msg.data='hello'
        self.publisher.publish(msg)
        
        # Stop the node immediately after publishing the message
        self.get_logger().info("Message published. Shutting down node.")
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = GoalSub()
    rclpy.spin(node)  # This will only run once because the node will be shut down after publishing the message
    rclpy.shutdown()
if __name__ == '__main__':
    main()
