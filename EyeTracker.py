import cv2
import autopy
from matplotlib import pyplot as plt
import seaborn as sns
import time

ESCAPE_KEY = 27
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)


face_cascade = cv2.CascadeClassifier("cascades/frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("cascades/righteye_2splits.xml")

video_capture = cv2.VideoCapture(0)
eye_x_positions = list()
eye_y_positions = list()

screen_resolution = autopy.screen.size()
if video_capture.isOpened():
    video_resolution = (video_capture.get(cv2.CAP_PROP_FRAME_WIDTH), video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT),)
else:
    video_resolution = None

x_max = 200
x_min = 150
y_max = 170
y_min = 125

distracted = 0
distracted_max = 20
distracted_total = 0
attention = 0

while 1:
    start = time.time()
    try:
        success, image = video_capture.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        eyes = eye_cascade.detectMultiScale(gray)

        for (eye_x, eye_y, eye_width, eye_height) in eyes:
            cv2.rectangle(img = image,  pt1 = (eye_x, eye_y),  pt2 = (eye_x + eye_width, eye_y + eye_height),  color = GREEN,  thickness = 2)
            roi_gray2 = gray[eye_y: eye_y + eye_height, eye_x: eye_x + eye_width]
            roi_color2 = image[eye_y: eye_y + eye_height, eye_x: eye_x + eye_width]

            hough_circles = cv2.HoughCircles(roi_gray2, cv2.HOUGH_GRADIENT, 1, 200, param1 = 200, param2 = 1, minRadius = 0, maxRadius = 0)

            eye_x_pos = (eye_x + eye_width) / 2
            eye_y_pos = (eye_y + eye_height) / 2

            print(eye_x_pos, eye_y_pos)

            eye_x_positions.append(eye_x_pos)
            eye_y_positions.append(eye_y_pos)

        cv2.imshow('img', image)

        if eye_x_pos < x_min or eye_x_pos > x_max or eye_y_pos < y_min or eye_x_pos > y_max or eye_x_pos is None or eye_y_pos is None:
            distracted = distracted + 1
            if distracted > fps_wait:
                print("YOU ARE DISTRACTED")
        else:
            distracted = 0

        end = time.time()
        total_time = end - start
        fps = 1 / total_time
        fps_wait = fps # 1 second

        key_pressed = cv2.waitKey(30) & 0xff
        if key_pressed == ESCAPE_KEY:
            break
    except Exception as e:
        print(e)

video_capture.release()
cv2.destroyAllWindows()
data = list(zip(eye_x_positions, eye_y_positions))

print(data)
print(attention, distracted_total)

plt.scatter(eye_x_positions, eye_y_positions)
plt.show()
sns.set()
