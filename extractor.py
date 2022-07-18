import ast
import cv2 as cv
from froperator import Operator
    
class Extractor:
    n = 0
    
    # Reads fields of message received from a consumer
    def readMessage(self, message):
        message = message.decode('utf-8')
        message = ast.literal_eval(message)
        ref = "ref/videos/" + message["video_ref"]
        time = message["frame_seconds_index"]
        op = message["op_type"]
        return ref, time, op
        
    # Captures frame specified by the message and sends it to the operator
    def extract(self, message):
        ref, time, op = self.readMessage(message)
        
        videoCap = cv.VideoCapture(ref)
        if not videoCap.isOpened():
            print(f"{self.n}: Couldnt open video {ref}")
            
        time = self.calculatePosition(time, videoCap)
        success = videoCap.set(cv.CAP_PROP_POS_MSEC, time*1000)
        if not success:
            print(f"{self.n}: Couldnt set position {time}s  in video {ref}")  
    
        success, image = videoCap.read()
        if success:
            self.requireOperation(image, op)
            #cv.imwrite("ref/frames/frame%d.jpg" %self.n, image)
            print(f"{self.n}: Successfully extracted frame {time}s  in video {ref}")
        else:
            print(f"{self.n}: Couldnt read frame in {time}s from video {ref}")  

        self.n += 1
        
    # If "time" is bigger than the video duration, truncates it to the last position of the video
    def calculatePosition(self, time, videoCap):
        n_frames = videoCap.get(cv.CAP_PROP_FRAME_COUNT)
        rate = videoCap.get(cv.CAP_PROP_FPS)
        duration = n_frames/rate
        if time > duration:
            print(f"{self.n}: Time required is bigger than video duration")
            time = duration
        videoCap.set(cv.CAP_PROP_POS_FRAMES, 0)
        return time
          
    # Builds connection with a frame operator
    def connect(self, opr):
        self.operator = opr
        
    # Sends image to operator, asking the proper operation
    def requireOperation(self, image, op):
        if "random_rotation" in op:
            self.operator.randomRotation(image, self.n)
        elif "flip" in op:
            self.operator.flip(image, self.n)
        elif "noise" in op:
            self.operator.noise(image, self.n)
        elif "grayscale" in op:
            self.operator.grayscale(image, self.n)