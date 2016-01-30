import cv2
import time

# for debug
from IPython import embed
from IPython.terminal.embed import InteractiveShellEmbed
ishell = InteractiveShellEmbed()

WIDTH = 320
HEIGHT = 240

# Capture Camera
cap = cv2.VideoCapture(0)
if cap.isOpened() is False:
    exit
    raise("Camera is not available.")

# edge detection
def edge(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Canny(gray_image, 100, 200)

cap.set(3, WIDTH)
cap.set(4, HEIGHT)

last_sec = time.ctime()
fps = 0

while(cap.isOpened()):
    # read 1 frame
    ret, frame = cap.read()
    if ret == False:
        continue

    t = time.ctime()
    if t != last_sec:
        print("Fps", fps)
        fps = 0
        last_sec = t

    fps += 1

    # show edge detection
    edge_image = edge(frame)
    #ishell()
    cv2.imshow("edge", edge(frame))

    # exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# close and finish
cap.release()
cv2.destroyAllWindows()
