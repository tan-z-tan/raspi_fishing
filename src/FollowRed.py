import cv2
import time
import numpy as np
from ParticleFilter import ParticleFilter 

# for debug
from IPython import embed
from IPython.terminal.embed import InteractiveShellEmbed
ishell = InteractiveShellEmbed()

WIDTH = 320
HEIGHT = 240

### PF
def evaluate(p):
    g, b, r = frame[p[0]][p[1]]
    red_degree = 2 * r - g - b
    # return np.exp(red_degree)
    return max(red_degree + 10, 0)

def next_state(p):
    next_vec = np.random.randn(2)
    next_y = p[0] + int(20 * next_vec[0])
    if next_y < 0:
        next_y = HEIGHT - 1
    if next_y >= HEIGHT:
        next_y = 0
    next_x = p[1] + int(20 * next_vec[1])
    if next_x < 0:
        next_x = WIDTH - 1
    if next_x >= WIDTH:
        next_x = 0
    return [next_y, next_x]

def initial_state(_):
    rand_state = np.random.rand(2)
    return [int(rand_state[0] * HEIGHT), int(rand_state[1] * WIDTH)]

pf = ParticleFilter(size = 1000, evaluate = evaluate, next_state = next_state, initial_state = initial_state)

pf.initialize()
### end PF

def camera_check():
    # Capture Camera
    if cap.isOpened() is False:
        return False
        raise("Camera is not available.")
    if cap.set(3, WIDTH) is False:
        return False
    if cap.set(4, HEIGHT) is False:
        return False
    return True

# edge detection
def edge(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Canny(gray_image, 100, 200)

cap = cv2.VideoCapture(0)
if camera_check() is False:
    exit

## start following
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
    # edge_image = edge(frame)
    # cv2.imshow("edge", edge(frame))

    pf.step()
    for p in pf.particle_list:
        y = p[0]
        x = p[1]
        cv2.rectangle(frame, (x, y), (x + 1, y), (0, 255, 0), 1)
    estimate = pf.estimate();
    print "Estimate ", pf.current_step, estimate
    cv2.rectangle(frame, (int(estimate[1]), int(estimate[0])), (int(estimate[1]) + 1, int(estimate[0]) + 1), (0, 0, 255), 3)

    cv2.imshow("video", frame)

    # exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# close and finish
cap.release()
cv2.destroyAllWindows()
