import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose
from visualization_msgs.msg import MarkerArray

class SpatialBoundingBoxSubscriber(Node):

    def __init__(self):
        super().__init__('spatial_bb_subscriber')
        self.subscription = self.create_subscription(
            MarkerArray,
            '/spatial_bb',
            self.spatial_bb_callback,
            10)
        self.publisher = self.create_publisher(Pose, '/person_pose', 10)

    def spatial_bb_callback(self, msg):
        for marker in msg.markers:
            if marker.text == 'person':
                pose_msg = Pose()
                pose_msg.position = marker.pose.position
                pose_msg.orientation = marker.pose.orientation
                self.publisher.publish(pose_msg)
                self.get_logger().info("Published person's pose.")

def main(args=None):
    rclpy.init(args=args)
    node = SpatialBoundingBoxSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
