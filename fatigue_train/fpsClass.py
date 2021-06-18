import time
import logging
import cv2
class runWithFPS():
    def __init__(self):
        self.FPS = [0.067]*30
    def start(self):
        self.begin = time.time()
    def frameTime(self):
        return sum(self.FPS)/len(self.FPS)
    def deltaTime(self, nameSting=""):
        logging.debug(f"{nameSting}: "+ str(time.time() - self.begin))
    def end(self, frame):
        deltaT = time.time() - self.begin
        self.FPS.append(deltaT)
        self.FPS = self.FPS[1:]
        cv2.putText(frame, f'FPS: {len(self.FPS)/sum(self.FPS):.1f}', (30, 30), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 0), 1)
        # return 