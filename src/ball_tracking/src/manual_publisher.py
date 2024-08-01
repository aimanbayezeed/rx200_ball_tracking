#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np

grid_size = 3
detected = 0

# Function to detect red color
def detect_red(frame):
    # Convert image to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define lower and upper bounds for red color detection
    lower_red = np.array([40, 100, 100])  # Lower bound for bright red
    upper_red = np.array([80, 255, 255])  # Upper bound for bright red
    
    # Mask image to extract red regions
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    # Apply morphological operations to remove noise
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    return mask

# Function to find the box where the center of the ball is located
def find_box(x, y, rows, cols):
    box_width = cols // grid_size
    box_height = rows // grid_size
    
    box_col = x // box_width
    box_row = y // box_height
    
    return box_row, box_col

def publish_coordinates():
    rospy.init_node('ball_grid_publisher', anonymous=True)
    image_pub = rospy.Publisher('detected_coordinates_image', Image, queue_size=10)
    row_pub = rospy.Publisher('box_row', Int32, queue_size=10)
    col_pub = rospy.Publisher('box_col', Int32, queue_size=10)
    detected_pub = rospy.Publisher('detected', Int32, queue_size=10)  # New publisher for 'detected' value
    bridge = CvBridge()
    rate = rospy.Rate(10)  # 10hz

    cap = cv2.VideoCapture(2)  # Open webcam
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while not rospy.is_shutdown():
        ret, frame = cap.read()  # Read frame from webcam
        if not ret:
            break

        rows, cols, _ = frame.shape

        # Detect red color
        red_mask = detect_red(frame)

        # Find contours in the red mask
        contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # Calculate the center of the contour
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                # Find the box where the center of the ball is located
                box_row, box_col = find_box(cX, cY, rows, cols)

                # Publish the box_row and box_col values
                row_pub.publish(box_row)
                col_pub.publish(box_col)

                # Publish the detected coordinates as an Image message
                try:
                    image_pub.publish(bridge.cv2_to_imgmsg(frame, "bgr8"))
                except CvBridgeError as e:
                    print(e)
        # Draw grid lines
        for i in range(1, grid_size):
            cv2.line(frame, (0, i * (rows // grid_size)), (cols, i * (rows // grid_size)), (0, 255, 0), 1)
            cv2.line(frame, (i * (cols // grid_size), 0), (i * (cols // grid_size), rows), (0, 255, 0), 1)
        
        # Show the original frame
        # cv2.imshow('Original Frame', frame)
        flipped_frame = cv2.flip(frame, 1)
        cv2.imshow('Original Frame', flipped_frame)
        
        # Show the filtered red image
        # cv2.imshow('Filtered Red', red_mask)
        flipped_red = cv2.flip(red_mask, 1)
        cv2.imshow('Filtered Red', flipped_red)

        # Check if contours are detected
        if len(contours) > 0:
            detected = 1
        else:
            detected = 0
        
        # Publish the value of 'detected'
        detected_pub.publish(detected)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        rate.sleep()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        publish_coordinates()
    except rospy.ROSInterruptException:
        pass
