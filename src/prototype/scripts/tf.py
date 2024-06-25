import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseArray,Pose
from tf2_ros import TransformBroadcaster

class TFPublisherNode(Node):
    def __init__(self):
        super().__init__('Odom_tf_publisher')
        self.tf_broadcaster = TransformBroadcaster(self)
        self.subscription = self.create_subscription(
            PoseArray,
            '/aruco_poses',
            self.odom_callback,
            10
        )

    def odom_callback(self, msg):
        for pose in msg.poses:
            x = pose.position.x
            y = pose.position.y
            z = pose.position.z
            qx = pose.orientation.x
            qy = pose.orientation.y
            qz = pose.orientation.z
            qw = pose.orientation.w

        # Create a TransformStamped message for the TF
        tf_msg = TransformStamped()
        tf_msg.header.stamp = msg.header.stamp
        tf_msg.header.frame_id = 'camera_link_optical'
        tf_msg.child_frame_id = 'ar_marker'

        # Set the translation
        tf_msg.transform.translation.x = z
        tf_msg.transform.translation.y = x
        tf_msg.transform.translation.z = y

        # Set the rotation (quaternion)
        tf_msg.transform.rotation.x = qz
        tf_msg.transform.rotation.y = -qw
        tf_msg.transform.rotation.z = -qy
        tf_msg.transform.rotation.w = qx

        # Publish the TF
        self.tf_broadcaster.sendTransform(tf_msg)


def main(args=None):
    rclpy.init(args=args)
    node = TFPublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
