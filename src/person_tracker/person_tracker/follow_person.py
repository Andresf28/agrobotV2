# Copyright 2023 Josh Newans
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist
import time

class FollowPerson(Node):

    def __init__(self):
        super().__init__('follow_person')
        self.subscription = self.create_subscription(
            Point,
            'detected_person',
            self.listener_callback,
            10)
        self.publisher_ = self.create_publisher(Twist, 'diff_drive_controller/cmd_vel_unstamped', 10) #/smd_vel


        self.declare_parameter("rcv_timeout_secs", 1.0)
        self.declare_parameter("angular_chase_multiplier", 0.7)
        self.declare_parameter("forward_chase_speed", 0.2)          # VELCIDAD HACIA ADELNATE, ORIGINAL EN 0.1
        self.declare_parameter("search_angular_speed", 1.0)
        self.declare_parameter("max_size_thresh", 0.5)              # cambiar para ver si ahora si camina origin 0.1
        self.declare_parameter("filter_value", 0.9)


        self.rcv_timeout_secs = self.get_parameter('rcv_timeout_secs').get_parameter_value().double_value
        self.angular_chase_multiplier = self.get_parameter('angular_chase_multiplier').get_parameter_value().double_value
        self.forward_chase_speed = self.get_parameter('forward_chase_speed').get_parameter_value().double_value
        self.search_angular_speed = self.get_parameter('search_angular_speed').get_parameter_value().double_value
        self.max_size_thresh = self.get_parameter('max_size_thresh').get_parameter_value().double_value
        self.filter_value = self.get_parameter('filter_value').get_parameter_value().double_value


        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.target_val = 0.0
        self.target_dist = 0.0
        self.lastrcvtime = time.time() - 10000

    def timer_callback(self):
        msg = Twist()
        if (time.time() - self.lastrcvtime < self.rcv_timeout_secs):
            self.get_logger().info('Target: {}'.format(self.target_val))
            print(self.target_dist)
            if (self.target_dist < self.max_size_thresh):
                msg.linear.x = self.forward_chase_speed
            msg.angular.z = -self.angular_chase_multiplier*self.target_val
        else:
            self.get_logger().info('Target lost')
            msg.angular.z = self.search_angular_speed
        self.publisher_.publish(msg)

    def listener_callback(self, msg):
        f = self.filter_value
        self.target_val = self.target_val * f + msg.x * (1-f)
        self.target_dist = self.target_dist * f + msg.z * (1-f)
        self.lastrcvtime = time.time()
        # self.get_logger().info('Received: {} {}'.format(msg.x, msg.y))


def main(args=None):
    rclpy.init(args=args)
    follow_person = FollowPerson()
    rclpy.spin(follow_person)
    follow_person.destroy_node()
    rclpy.shutdown()
