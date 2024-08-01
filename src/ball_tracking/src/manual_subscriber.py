#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32
from interbotix_xs_modules.arm import InterbotixManipulatorXS
import numpy as np

desired_z = 2
desired_r = 2
grid_size = 3
detected = False
box_row = 0 
box_col = 0
prev_box_row = None  # Previous value of box_row
prev_box_col = None  # Previous value of box_col


def arm_control_callback_row(data):
    global box_row
    box_row = data.data
    return box_row


def arm_control_callback_col(data):
    global box_col
    box_col = data.data
    return box_col


def detected_callback(data):
    global bot
    global detected

    if bot is None:
        rospy.logerr('Bot is not initialized!')
        return

    detected_0 = data.data

    if detected_0 == 0:
        detected = False
        # bot.arm.set_ee_pose_components(x=0.3, z=0.2)
        pass
    elif detected_0 == 1:
        detected = True
        execute_commands()

    ## alternate method
    # while detected_0:
    #     detected = True
    #     execute_commands()
    #     user_input = input("Press 'h' to break the loop: ").lower()
    #     if user_input == 'h':
    #         break  # break out of the loop

    # detected = False 
    # bot.arm.set_ee_pose_components(x=0.3, z=0.2)

    return detected


def execute_commands():
    global prev_box_row
    global prev_box_col

    # Check if the new values of box_row and box_col are different from the previous ones
    # if box_row != prev_box_row or box_col != prev_box_col:
    #     # Update the previous values
    #     prev_box_row = box_row
    #     prev_box_col = box_col
        
    #     # Execute the commands based on the new values
    #     if box_row == 0:
    #         bot.arm.set_ee_pose_components(x=0.3, z=0.35)
    #     elif box_row == 1:
    #         bot.arm.set_ee_pose_components(x=0.3, z=0.2)
    #     elif box_row == 2:
    #         bot.arm.set_ee_pose_components(x=0.3, z=0.15)
    #     if box_col == 0:
    #         bot.arm.set_single_joint_position("waist", 30 * (np.pi / 180))
    #     elif box_col == 1:
    #         bot.arm.set_single_joint_position("waist", 0 * (np.pi / 180))
    #     elif box_col == 2:
    #         bot.arm.set_single_joint_position("waist", -30 * (np.pi / 180))


    if box_row != prev_box_row:
        prev_box_row = box_row
        # Execute the commands based on the new values
        if box_row == 0:
            bot.arm.set_ee_pose_components(x=0.3, z=0.35)
        elif box_row == 1:
            bot.arm.set_ee_pose_components(x=0.3, z=0.2)
        elif box_row == 2:
            bot.arm.set_ee_pose_components(x=0.3, z=0.15)
    if box_col != prev_box_col:
        if box_col == 0:
            bot.arm.set_single_joint_position("waist", 30 * (np.pi / 180))
        elif box_col == 1:
            bot.arm.set_single_joint_position("waist", 0 * (np.pi / 180))
        elif box_col == 2:
            bot.arm.set_single_joint_position("waist", -30 * (np.pi / 180))


if __name__ == '__main__':
    bot = InterbotixManipulatorXS("rx200", "arm", "gripper")  # Initialize bot here
    bot.arm.set_ee_pose_components(x=0.3, z=0.2)  # x position is fixed since no depth info
    rospy.Subscriber('detected', Int32, detected_callback)  # Subscribe to 'detected' topic
    rospy.Subscriber('box_row', Int32, arm_control_callback_row)
    rospy.Subscriber('box_col', Int32, arm_control_callback_col)

    print("spin")

    rospy.spin()
