import cv2
import time
import numpy as np
import threading
from ParticleFilter import ParticleFilter 

# for debug
from IPython import embed
from IPython.terminal.embed import InteractiveShellEmbed
ishell = InteractiveShellEmbed()

WIDTH = 320
HEIGHT = 240

### Define function required for PF tracking
def evaluate(p):
    g, b, r = frame[p[0]][p[1]]
    red_degree = 2 * r - g - b
    # return np.exp(red_degree)
    return max(red_degree + 10, 0) + 1

def next_state(p):
    next_vec = np.random.randn(2) * [10, 10]
    next_y = (p[0] + int(next_vec[0]) + 2 * HEIGHT + 1) % HEIGHT - 1
    next_x = (p[1] + int(next_vec[1]) + 2 * WIDTH + 1) % WIDTH - 1
    return [next_y, next_x]

def initial_state(_):
    return np.random.rand(2) * [HEIGHT, WIDTH]

pf = ParticleFilter(size = 1000, evaluate = evaluate, next_state = next_state, initial_state = initial_state)

pf.initialize()
### end PF

class CVProcess(threading.Thread):
    def __init__(self, window_name, pf):
        threading.Thread.__init__(self)
        threading.Thread.daemon = True
        self.window_name = window_name
        self.pf = pf
        self.frame = None

        self.available = self.camera_check()

    def camera_check(self):
        self.cap = cv2.VideoCapture(0)

        # Capture Camera
        if self.cap.isOpened():
            self.cap.set(3, WIDTH)
            self.cap.set(4, HEIGHT)
            time.sleep(2) # camera might take 1 or 2 second to change parameters
            return True
        else:
            raise("Camera is not available.")
            return False

    def run(self):
        while True:
            if self.frame != None:
                current_frame = self.frame
                for p in self.pf.particle_list:
                    y = int(p[0])
                    x = int(p[1])
                    cv2.rectangle(current_frame, (x, y), (x + 1, y), (0, 255, 0), 1)
                estimate = self.pf.estimate()
                cv2.rectangle(current_frame, (int(estimate[1]), int(estimate[0])), (int(estimate[1]) + 1, int(estimate[0]) + 1), (0, 0, 255), 3)
                cv2.imshow(self.window_name, current_frame)
            time.sleep(0.5)

    def get_frame(self):
        status, frame = self.cap.read()
        self.frame = frame
        return status, frame

if __name__ == "__main__":
    cv_process = CVProcess('tracking', pf)
    if cv_process.available == False:
        exit

    last_sec = time.ctime()
    fps = 0
    cv_process.start()

    while True:
        ret, frame = cv_process.get_frame()
        if ret == False:
            continue

        t = time.ctime()
        if t != last_sec:
            print("Fps", fps)
            fps = 0
            last_sec = t

        fps += 1

        pf.step()

        estimate = pf.estimate()
        print "Estimate ", pf.current_step, estimate

        # exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # release all resources
    cap.release()
    cv2.destroyAllWindows()
