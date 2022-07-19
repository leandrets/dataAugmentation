import random
import cv2 as cv

class Operator:
    
    def randomRotation(self, image):
        rows, cols, n = image.shape
        angle = random.random() * 180
        matrix = cv.getRotationMatrix2D(((cols-1)/2, (rows-1)/2), angle, 1)
        result = cv.warpAffine(image, matrix, (cols, rows))
        return result, angle
        
    def flip(self, image):
        result = cv.flip(image, 0)
        return result

    def noise(self, image):
        return image
    
    def grayscale(self, image):
        result = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        return result
    