from Webcam import Webcam
import cv2
import numpy as np
import math

camera = Webcam()
left_top_corner = (int(camera.width * 0.8), int(camera.height * 0.4))
left_bot_corner = (int(camera.width * 0.8), int(camera.height * 0.5))
right_top_corner = (int(camera.width * 0.9), int(camera.height * 0.4))
right_bot_corner = (int(camera.width * 0.9), int(camera.height * 0.5))
top = (int(camera.width * 0.85), int(camera.height * 0.4))
bot = (int(camera.width * 0.85), int(camera.height * 0.5))
up_is_pushed = False
down_is_pushed = False
left_is_pushed = False
right_is_pushed = False

def hsv_extraction(frame):
    frame = cv2.medianBlur(frame, 5)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([100, 150, 50])
    upper_blue = np.array([150, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    blue_image = cv2.bitwise_and(hsv, hsv, mask=mask)
    frame = cv2.cvtColor(blue_image, cv2.COLOR_HSV2BGR)
    edges_frame = cv2.Canny(frame, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges_frame, 1, np.pi / 180, 20)
    if lines is not None:
        for rho, theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 - 1000 * b)
            y1 = int(y0 + 1000 * a)
            x2 = int(x0 + 1000 * b)
            y2 = int(y0 - 1000 * a)
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        return (rho, theta), frame
    return (1000, 1000), frame

while True:
    frame = camera.get_current_frame()
    (rho, theta), line_frame = hsv_extraction(frame)
    # blue_channel = frame[:, :, 2]
    if 0 > theta > 1.58:
        if math.fabs(rho) < camera.width / 2:
            up_is_pushed = True
            down_is_pushed = False
            left_is_pushed = False
            right_is_pushed = False
        elif math.fabs(rho) > camera.width / 2:
            if up_is_pushed and right_is_pushed:
                down_is_pushed = True
                right_is_pushed = False
                up_is_pushed = False
                left_is_pushed = True
            else:
                up_is_pushed = True
                left_is_pushed = False
                down_is_pushed = False
                right_is_pushed = True
    else:
        if math.fabs(rho) < camera.width / 2:
            if up_is_pushed and left_is_pushed:
                down_is_pushed = True
                left_is_pushed = False
                up_is_pushed = False
                right_is_pushed = True
            else:
                up_is_pushed = True
                right_is_pushed = False
                left_is_pushed = True
                down_is_pushed = False
        elif math.fabs(rho) > camera.width / 2:
            up_is_pushed = True
            down_is_pushed = False
            left_is_pushed = False
            right_is_pushed = False
    if up_is_pushed and not down_is_pushed and not left_is_pushed and not right_is_pushed:
        cv2.arrowedLine(line_frame, bot, top, (0, 0, 255), 5)
    elif up_is_pushed and left_is_pushed and not right_is_pushed and not down_is_pushed:
        cv2.arrowedLine(line_frame, right_bot_corner, left_top_corner, (0, 0, 255), 5)
    elif up_is_pushed and right_is_pushed and not left_is_pushed and not down_is_pushed:
        cv2.arrowedLine(line_frame, left_bot_corner, right_top_corner, (0, 0, 255), 5)
    elif down_is_pushed and left_is_pushed and not right_is_pushed and not up_is_pushed:
        cv2.arrowedLine(line_frame, right_top_corner, left_bot_corner, (0, 0, 255), 5)
    elif down_is_pushed and right_is_pushed and not left_is_pushed and not up_is_pushed:
        cv2.arrowedLine(line_frame, left_top_corner, right_bot_corner, (0, 0, 255), 5)
    print(up_is_pushed)
    print(down_is_pushed)
    print(left_is_pushed)
    print(right_is_pushed)
    cv2.imshow('asd', line_frame)
    cv2.waitKey(1)