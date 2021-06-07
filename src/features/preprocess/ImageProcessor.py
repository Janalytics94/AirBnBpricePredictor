#!/usr/bin/env python3
import cv2
import glob
from PIL import Image, ImageStat
import numpy as np

class ImageProcessor():
    ''' Class contians method of feature extraction for the images. We want to load images and extract
    Red, Blues and Greens, as well as image data like size etc and brighness '''
    
    def getImage(self,path):
        
        image = cv2.imread(path)
        
        return image
        
    def imgDetails(self,img):
        # accepts an image of format -> cv2.imread('image path')
        height, width, channels = img.shape
        pixels = img.size
        size = [height,width]
        return size, channels, pixels

    def channelSplit(self,img):
        # accepts an image of format -> cv2.imread('image path')
        [B,G,R] = np.dsplit(img,img.shape[-1])
        blue = np.mean(B)
        green = np.mean(G)
        red = np.mean(R)
        
        return blue, green, red

    def getBrightness(self,img):
        # opens image in current working directory, converts to greyscale, and pulls a float value for brightness
        img_src = Image.fromarray(img).convert('L')
        stat = ImageStat.Stat(img_src)
        brightness = stat.mean[0]
        
        return brightness