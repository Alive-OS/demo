#!/usr/bin/env python3
# *************************************************************************
#
# Copyright (c) 2021 Andrei Gramakov. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# site:    https://agramakov.me
# e-mail:  mail@agramakov.me
#
# *************************************************************************
from aliveos_hw.abstract_device import AbstractDevice
import os
from time import sleep
from random import randrange
from rospy import logwarn, logerr, loginfo, logdebug
from aliveos_py.ros import get
from geometry_msgs.msg import Twist


class SimpleDevice(AbstractDevice):
    def main(self):
        self.pub_robot_movements = get.publisher("cmd_vel", Twist)
        i = 0
        while (1):
            if not i % 5:
                self.publish_device_data(data_value=101)
            if not i % 11:
                self.publish_device_data(data_value=102)
            self.publish_device_data(data_value=randrange(-100, 100, 1))
            sleep(1)
            i += 1

    def publish_movement(self, line_x, line_y, line_z, ang_x, ang_y, ang_z):
        m = Twist()
        m.linear.x = line_x
        m.linear.y = line_y
        m.linear.z = line_z
        m.angular.x = ang_x
        m.angular.y = ang_y
        m.angular.z = ang_z
        self.pub_robot_movements.publish(m)

    def command_move(self, arg_list):
        logdebug("command_move")
        duration = None
        for a in arg_list:
            try:
                duration = int(a)
                break
            except ValueError:
                pass

        if "left" in arg_list:
            logdebug("Move left")
            self.publish_movement(0, 0, 0, 0, 0, 1.5)
            # sleep(0.3)
            # self.publish_movement(0, 0, 0, 0, 0, 0)
        elif "right" in arg_list:
            logdebug("Move right")
            self.publish_movement(0, 0, 0, 0, 0, -1.5)
            # sleep(0.3)
            # self.publish_movement(0, 0, 0, 0, 0, 0)
        elif "forward" in arg_list:
            logdebug("Move forward")
            self.publish_movement(0.4, 0, 0, 0, 0, 0)
            # sleep(0.3)
            # self.publish_movement(0, 0, 0, 0, 0, 0)
        elif "backward" in arg_list:
            logdebug("Move backward")
            self.publish_movement(-0.4, 0, 0, 0, 0, 0)
            # sleep(0.3)
            # self.publish_movement(0, 0, 0, 0, 0, 0)
        else:
            logerr("Move command has no direction: left, right, forward or backward")
            return

        if duration:
            logwarn(f"Wait for {duration} sec")
            logwarn("Stop")

    def command_stop(self, arg_list):
        self.publish_movement(0, 0, 0, 0, 0, 0)


d = SimpleDevice(
    dev_name="simple_device",
    #  hw_server_name="simple_hw_server",
    hw_server_name=None,
    perception_concept_descriptor_json=f"{os.path.dirname(__file__)}/" + "simple_device _pc_dsc.json",
    emotion_core_data_descriptor_json="""
{
    "$schema": "perception-concept-descriptor.json",
    "data_type": "value",
    "value_min": 0,
    "value_max": 100,
    "weights": [
        { "parameter": "adrenaline", "value": -0.1 },
        { "parameter": "dopamine", "value": 2 }
    ]
}
    """)
d.start()
