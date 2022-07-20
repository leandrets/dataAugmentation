import random
import numpy as np
import cv2 as cv

SCALE = 1
X_AXIS = 0

class Operator:
    
    # Rotates the image a random amount of degrees, around its center.
    def randomRotation(self, image):
        shape = image.shape
        rows = shape[0]
        cols = shape[1]
        angle = random.random() * 180
        matrix = cv.getRotationMatrix2D(((cols-1)/2, (rows-1)/2), angle, SCALE)
        result = cv.warpAffine(image, matrix, (cols, rows))
        return result, angle
        
    # Flips the image over the X axis.
    def flip(self, image):
        return cv.flip(image, X_AXIS)

    # Adds Gaussian noise to the image.
    def noise(self, image):
        shape = image.shape
        mean = 0
        sigma = 75
        gaussian = np.random.normal(mean, sigma, shape)
        gaussian = gaussian.reshape(shape)
        result = image + gaussian
        return result
    
    # Converts colored image to grayscale.
    def grayscale(self, image):
        return cv.cvtColor(image, cv.COLOR_BGR2GRAY)
         
    