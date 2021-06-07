#! /usr/bin/env python3
import os
import pandas as pd
import numpy as np
import json
import sys
import io
sys.path.append('.')
import src.features.preprocess.ImageProcessor as ImageProcessor
from clize import run
from wand.image import Image

def convert_images(source, df_name, target):
    image_processor = ImageProcessor()

    all_images = os.listdir(os.path.join(source, df_name))
    with open(target, 'w') as output_stream:
        for image in all_images:
            img = image_processor.getImage(os.path.join(source + '/' + df_name + image))
            imgData  = image_processor.imgDetails(img)
            brightness = image_processor.getBrightness(img)
            colors_BGR = image_processor.channelSplit(img)
            json.dump(
                {
                    'Data': imgData,
                    'Brightness': brightness,
                    'BGR': colors_BGR
                }, output_stream
            )
            output_stream.write('\n')

if __name__ == '__main__':
    run(convert_images)   
    