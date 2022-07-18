import av
import ast
import cv2 as cv
    
class Extractor:
    n = 0
    
    def readMessage(self, message):
        message = message.decode('utf-8')
        message = ast.literal_eval(message)
        ref = "ref/videos/" + message["video_ref"]
        time = message["frame_seconds_index"]
        op = message["op_type"]
        return ref, time, op
        
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
            cv.imwrite("ref/frames/frame%d.jpg" %self.n, image)
            print(f"{self.n}: Successfully extracted frame {time}s  in video {ref}")
        else:
            print(f"{self.n}: Couldnt read frame in {time}s from video {ref}")  

        self.n += 1
        
    def calculatePosition(self, time, videoCap):
        n_frames = videoCap.get(cv.CAP_PROP_FRAME_COUNT)
        videoCap.set(cv.CAP_PROP_POS_FRAMES, n_frames)
        duration = videoCap.get(cv.CAP_PROP_POS_MSEC)
        if time > duration:
            print(f"{self.n}: Time required is bigger than video duration")
            time = duration
        videoCap.set(cv.CAP_PROP_POS_FRAMES, 0)
        return time
          