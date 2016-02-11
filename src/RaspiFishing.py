import cv2
import time
import numpy as np
from ParticleFilter import ParticleFilter 
from Motor import Motor

# for debug
from IPython import embed
from IPython.terminal.embed import InteractiveShellEmbed
ishell = InteractiveShellEmbed()

WIDTH = 320
HEIGHT = 240

### Define function required for PF tracking
def evaluate(p):
    sigma = 50.0;
    g, b, r = frame[p[0]][p[1]]
    if False:
        dist = np.sqrt (b * b + g * g + (255.0 - r) * (255.0 - r));
        val = 1.0 / (np.sqrt (2.0 * np.pi) * sigma) * np.exp (-dist * dist / (2.0 * sigma * sigma));
        return val
    else:
        red_degree = 2 * r - g - b
        # return 1.0 / (np.sqrt(2 * np.pi) * sigma) * np.exp(-red_degree / 2 * sigma * sigma)
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

### Hit Detection ###
def hit(past_point_list):
    average_move = 0
    for i in range(1, len(past_point_list)):
        average_move += np.linalg.norm(past_point_list[i-1] - past_point_list[i]) / len(past_point_list)

    print "Average_move", average_move
    #return average_move > 3
    return average_move > 10

def camera_check():
    # Capture Camera
    if cap.isOpened() is False:
        return False
        raise("Camera is not available.")
    cap.set(3, WIDTH)
    cap.set(4, HEIGHT)
    time.sleep(2) # camera might take 1 or 2 second to change parameters
    return True

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    if camera_check() is False:
        exit
    # mode
    mode = "detect" # detect, fish, wait

    motor = Motor()
    status = "detect" # "attract", "fish", "wait"
    
    ## start following
    last_sec = time.ctime()
    fps = 0
    last_point_list = []
    display = True
    step = 0

    while(cap.isOpened()):
        step += 1

        if mode == "detect":
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

            pf.step()
            estimate = pf.estimate()
            last_point_list.insert(0, estimate)
            if len(last_point_list) >= 5:
                last_point_list = last_point_list[0:5]
                if step > 20 and hit(last_point_list):
                    print "Hit!!!!"
                    mode = "fish"
                    
            #print "Estimate ", pf.current_step, estimate

            if display and fps == 1:
                for p in pf.particle_list:
                    y = int(p[0])
                    x = int(p[1])
                    cv2.rectangle(frame, (x, y), (x + 1, y), (0, 255, 0), 1)
                cv2.rectangle(frame, (int(estimate[1]), int(estimate[0])), (int(estimate[1]) + 1, int(estimate[0]) + 1), (0, 0, 255), 3)

                cv2.imshow("video", frame)
        elif mode == "attract":
            motor.rotate_left(0.5)
            motor.rotate_right(0.5)
            mode = "detect"
            step = 0
        elif mode == "fish":
            motor.rotate_left(5)
            mode = "wait"
        else:
            # start detecting if 's' is pressed
            if cv2.waitKey(10) & 0xFF == ord('s'):
                mode = "detect"
                step = 0

    # stop motor
    motor.stop()

    # close and finish
    cap.release()
    cv2.destroyAllWindows()
