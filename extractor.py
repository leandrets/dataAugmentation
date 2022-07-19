import ast
import cv2 as cv
from froperator import Operator
import math
    
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
            print(f"    {self.n}: ERROR - couldnt open video {ref}")
            return
            
        time = self.calculatePosition(time, videoCap)
        success = videoCap.set(cv.CAP_PROP_POS_MSEC, time*1000)
        if not success:
            print(f"    {self.n}: ERROR - couldnt set position {time}s  in video {ref}")
            return
    
        success, image = videoCap.read()
        if success:
            print(f"        {self.n}: Successfully extracted frame {time}s  in video {ref}")
            self.requireOperation(image, op)
            #cv.imwrite("ref/frames/frame%d.jpg" %self.n, image)
        else:
            print(f"    {self.n}: ERROR - couldnt read frame in {time}s from video {ref}")
            return  

        self.n += 1
        
    # If "time" is bigger than the video duration, truncates it to the last position of the video
    def calculatePosition(self, time, videoCap):
        n_frames = videoCap.get(cv.CAP_PROP_FRAME_COUNT)
        rate = videoCap.get(cv.CAP_PROP_FPS)
        duration = math.floor(n_frames/rate)
        if time >= duration:
            print(f"    {self.n}: WARNING - time required is bigger than video duration")
            time = duration - 1
        videoCap.set(cv.CAP_PROP_POS_FRAMES, 0)
        return time
          
    # Builds connection with a frame operator
    def connect(self, opr):
        self.operator = opr
        
    # Sends image to operator, asking the proper operation
    def requireOperation(self, image, op):
        operations = 0
        if "random_rotation" in op:
            image, angle = self.operator.randomRotation(image)
            print(f"            {self.n}: Successfully rotated {angle} degrees")
            operations +=1
        if "flip" in op:
            image = self.operator.flip(image)
            print(f"            {self.n}: Successfully flipped")
            operations += 1
        if "noise" in op:
            image = self.operator.noise(image)
            print(f"            {self.n}: Successfully applied noise filter")
            operations += 1
        if "grayscale" in op:
            image = self.operator.grayscale(image)
            print(f"            {self.n}: Successfully converted to grayscale")
            operations += 1
        if operations == 0:
            print(f"                {self.n}: No operation made")
        else:
            cv.imwrite("ref/results/frame%d.jpg" % self.n, image)
            print(f"                {self.n}: Saved operated frame")