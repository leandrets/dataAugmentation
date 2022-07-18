import random
import cv2 as cv

class Operator:
    
    def randomRotation(self, image, counter):
        rows, cols, n = image.shape
        angle = random.random() * 180
        matrix = cv.getRotationMatrix2D(((cols-1)/2, (rows-1)/2), angle, 1)
        result = cv.warpAffine(image, matrix, (cols, rows))
        cv.imwrite("ref/results/frame%drotated.jpg" % counter, result)
        print(f"{counter}: Successfully rotated {angle} degrees")
        
    def flip(self, image, counter):
        pass

    def noise(self, image, counter):
        pass
    
    def grayscale(self, image, counter):
        pass
    