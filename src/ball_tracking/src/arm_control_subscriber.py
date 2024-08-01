#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32
from interbotix_xs_modules.arm import InterbotixManipulatorXS
import math
import time

desired_z = 2
desired_r = 2
grid_size = 5
detected = False
box_row = 0 
box_col = 0



def arm_control_callback_row(data):
    global bot, detected, box_row
    if bot is None:
        rospy.logerr('Bot is not initialized!')
        return

    box_row = data.data
    print("box_row:", box_row)  # Print box_row after updating
    error_z = desired_z - box_row
    print("error_z", error_z)
    z_correction = 0.05

    
    while detected:
        end_effector_pose = bot.arm.get_ee_pose()
        current_z = end_effector_pose[2, 3]
        print("CURRENT Z: ", current_z)
        print("error_z_inside", error_z)

        if current_z <= 0.40 and current_z > 0.09:
            if error_z > 0:
                bot.arm.set_ee_cartesian_trajectory(z=z_correction)
                print("error > 0")
                # rospy.sleep(10)
            elif error_z < 0:
                # bot.arm.set_ee_cartesian_trajectory(z=-z_correction)
                print("error < 0")
                # rospy.sleep(10)

            else:
                # bot.arm.set_ee_cartesian_trajectory(z=0)
                print("error = 0")
                # rospy.sleep(10)

        else:
            # bot.arm.set_ee_pose_components(x=0.3, z=0.2)
            print("going home")
            # rospy.sleep(10)
  
    # else:
    #     bot.arm.set_ee_pose_components(x=0.3, z=0.2)
    #     print("finally")
    

    return box_row

def arm_control_callback_col(data):
    global bot, detected, box_col
    if bot is None:
        rospy.logerr('Bot is not initialized!')
        return

    box_col = data.data
    # print("box_col:", box_col)  # Print box_col after updating
    
    # if detected:
    #     end_effector_pose = bot.arm.get_ee_pose()
    #     rotation_value = math.atan2(end_effector_pose[1, 0], end_effector_pose[0, 0])
    #     current_r = rotation_value * (180 / math.pi)
    #     r_correction = 5
    #     error_r = desired_r - box_col

    #     if error_r > 0:
    #         bot.arm.set_single_joint_position("waist", r_correction * (180 / math.pi))
    #     elif error_r < 0:
    #         bot.arm.set_single_joint_position("waist", -r_correction * (180 / math.pi))
    #     else:
    #         bot.arm.set_single_joint_position("waist", 0)
    # else:
    #     bot.arm.set_ee_pose_components(x=0.3, z=0.2)

    # rospy.Timer(rospy.Duration(2), lambda event: None, oneshot=True)
    return box_col



def detected_callback(data):
    global bot
    global detected
    if bot is None:
        rospy.logerr('Bot is not initialized!')
        return

    detected_0 = data.data
    # print("Detected:", detected_0)

    # Implement your logic based on the value of 'detected'
    if detected_0 == 0:
        detected = False
        # Do something if not detected
        pass
    elif detected_0 == 1:
        detected = True
        # Do something if detected
        pass
    
    return detected

if __name__ == '__main__':


    # rospy.init_node('arm_control_ball_subscriber', anonymous=True)
    bot = InterbotixManipulatorXS("rx200", "arm", "gripper")  # Initialize bot here
    bot.arm.set_ee_pose_components(x=0.3, z=0.2) # x position is fixed since no depth info
    rospy.Subscriber('detected', Int32, detected_callback)  # Subscribe to 'detected' topic
    rospy.Subscriber('box_row', Int32, arm_control_callback_row)
    rospy.Subscriber('box_col', Int32, arm_control_callback_col)
    print("spin")

    rospy.spin()
