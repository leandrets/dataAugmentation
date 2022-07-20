import random
import numpy as np
import cv2 as cv

class Operator:
    
    def randomRotation(self, image):
        shape = image.shape
        rows = shape[0]
        cols = shape[1]
        angle = random.random() * 180
        matrix = cv.getRotationMatrix2D(((cols-1)/2, (rows-1)/2), angle, 1)
        result = cv.warpAffine(image, matrix, (cols, rows))
        return result, angle
        
    def flip(self, image):
        return cv.flip(image, 0)

    def noise(self, image):
        shape = image.shape
        mean = 0
        sigma = 75
        gaussian = np.random.normal(mean, sigma, shape)
        gaussian = gaussian.reshape(shape)
        result = image + gaussian
        return result
    
    def grayscale(self, image):
        return cv.cvtColor(image, cv.COLOR_BGR2GRAY)
         
    