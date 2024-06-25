import rclpy
from rclpy.node import Node
import tf2_ros
from geometry_msgs.msg import TransformStamped,PoseStamped


class TFListenerNode(Node):
    def __init__(self):
        super().__init__('tf_listener_node')
        self.tf_buffer = tf2_ros.Buffer(cache_time=rclpy.duration.Duration(seconds=10))
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        self.publisher = self.create_publisher(PoseStamped, '/goal_pose', 10)


        self.map_frame = 'map'
        self.base_link_frame = 'object_link'

        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        try:

           # self.tf_buffer.wait_for_transform_async(self.map_frame,self.base_link_frame,time=rclpy.time.Time(seconds=4)
            #)
            transform_stamped = self.tf_buffer.lookup_transform(
                target_frame=self.map_frame,
                source_frame=self.base_link_frame,
                time=rclpy.time.Time(),  # Use latest available transform
                timeout=rclpy.duration.Duration(seconds=0.1)
            )

            self.handle_transform(transform_stamped)
        except tf2_ros.LookupException as e:
            self.get_logger().error(f"Transform lookup error: {e}")
        except tf2_ros.ExtrapolationException as e:
            self.get_logger().error(f"Transform extrapolation error: {e}")

    def handle_transform(self, transform_stamped):
        # Do something with the transformation
        pose_msg = PoseStamped()
        pose_msg.header.frame_id = "map"
        pose_msg.header.stamp.sec = 0
        pose_msg.header.stamp.nanosec = 0
        pose_msg.pose.position.x = transform_stamped.transform.translation.x
        pose_msg.pose.position.y = transform_stamped.transform.translation.y
        pose_msg.pose.position.z = 0.0
        pose_msg.pose.orientation.w = 1.0

        self.publisher.publish(pose_msg)

        self.get_logger().info(f"Transform between {transform_stamped.header.frame_id} and {transform_stamped.child_frame_id}:")
        self.get_logger().info(f"Translation: {transform_stamped.transform.translation}")
        self.get_logger().info(f"Rotation: {transform_stamped.transform.rotation}")

def main(args=None):
    rclpy.init(args=args)
    node = TFListenerNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
