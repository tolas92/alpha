import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, TransformStamped
from sensor_msgs.msg import Imu, LaserScan
from nav_msgs.msg import Odometry,OccupancyGrid
from tf2_ros import TransformBroadcaster
import math
from rclpy.qos import QoSProfile

class TFPublisherNode(Node):
    def __init__(self):
        super().__init__('Imu_tf_publisher')
        self.tf_broadcaster = TransformBroadcaster(self)
        self.odom_timestamp = None
        self.laser_timestamp = None
        
     
        self.subscription_odom = self.create_subscription(
            OccupancyGrid,
            '/map',
            self.odom_callback,
            10
        )
        
        self.subscription_laser = self.create_subscription(
            LaserScan,
            '/scan',
            self.laser_callback,
            10
        )
        
    def odom_callback(self, msg):
        self.odom_timestamp = msg.header.stamp
        self.print_timestamps()

    def laser_callback(self, msg):
        self.laser_timestamp = msg.header.stamp
        self.print_timestamps()

    def print_timestamps(self):
        if self.laser_timestamp is not None:
            print("Odometry Timestamp:", self.odom_timestamp)
            print("Laser Timestamp:", self.laser_timestamp)
            print("-----------------------------")  # Separator for clarity
    
def main(args=None):
    rclpy.init(args=args)
    node = TFPublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
