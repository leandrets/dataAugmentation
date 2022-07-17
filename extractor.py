import av
import ast

class Extractor:
    
    containers = {}
    streams = {}
    frameSets = {}
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
        
        if ref not in self.containers:
            self.containers[ref] = av.open(ref)
            self.streams[ref] = self.containers[ref].streams.video[0]
            self.frameSets[ref] = self.containers[ref].decode(self.streams[ref])
        
        frame_rate = int(self.streams[ref].average_rate)
        index = self.calculateIndex(time, frame_rate)
        
        sucess = False
        for idx, frame in enumerate(self.frameSets[ref]):
            if abs(idx-index) < 1:
                frame.to_image().save("ref/frames/frame%d.jpg" % self.n)
                print(f"{self.n}: Successfully extracted frame {index} of video {ref}")
                sucess = True
                break
        if not sucess:
            print(f"{self.n}: Failed to extract frame {index} of video {ref}")
        self.n += 1
        
    def calculateIndex(self, time, rate):
        return (time * rate) - 1
    