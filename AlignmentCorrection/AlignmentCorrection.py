#!/usr/bin/python
# -*- coding: utf-8 -*-
# import the necessary packages

import numpy as np
import cv2
import os
import pytesseract
import re
from datetime import datetime
import base64

# required when running it in windows os

pytesseract.pytesseract.tesseract_cmd = 'Tesseract-OCR/tesseract.exe'


class AlignmentCorrection:

    def __init__(self):
        pass

    def rotate_images(self, parr_image, pobj_logger):
        '''
            Method to rotate image using pytesseract osd which detects the orientation using the text in the image
            Input: parr_image - input image to be rotated
                   pobj_logger - logger object to log details
            Output:  rotated_image - rotated input image
        '''

        rot = 0
        try:
            rotated_image = parr_image
            gray_image = cv2.cvtColor(parr_image, cv2.COLOR_BGR2GRAY)
            gray_image = cv2.bitwise_not(gray_image)
            rot_data = pytesseract.image_to_osd(gray_image)
            rot = re.search('(?<=Rotate: )\d+', rot_data).group(0)
            if rot == '90':
                rotated_image = cv2.rotate(rotated_image,
                        cv2.cv2.ROTATE_90_CLOCKWISE)
            elif rot == '180':
                rotated_image = cv2.rotate(rotated_image,
                        cv2.cv2.ROTATE_180)
            elif rot == '270':
                rotated_image = cv2.rotate(rotated_image,
                        cv2.ROTATE_90_COUNTERCLOCKWISE)

            return (rotated_image, rot)
        except Exception as lobj_exception:
            return (rotated_image, rot)

    def deskew_images(
        self,
        parr_image,
        parr_original_image,
        pobj_logger,
        ):
        try:
            '''
            Method to deskew image by detecting the text alignment in the image
            Input: parr_image - preprocessed image
                   parr_original_image - original input image 
                   pobj_logger - logger object to log details
            Output:  rotated_image - rotated input image
            '''


            # convert the background to ensure foreground is now "white" and
            # the background is "black"

            gray = cv2.bitwise_not(parr_image)

            # threshold the image, setting all foreground pixels to
            # 255 and all background pixels to 0

            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY
                                   | cv2.THRESH_OTSU)[1]

            # grab the (x, y) coordinates of all pixel values that
            # are greater than zero, then use these coordinates to
            # compute a rotated bounding box that contains all
            # coordinates

            coords = np.column_stack(np.where(thresh > 0))
            angle = cv2.minAreaRect(coords)[-1]

            # the `cv2.minAreaRect` function returns values in the
            # range [-90, 0); as the rectangle rotates clockwise the
            # returned angle trends to 0 -- in this special case we
            # need to add 90 degrees to the angle

            if angle < -45:
                angle = -(90 + angle)
            else:

            # otherwise, just take the inverse of the angle to make
            # it positive

                angle = -angle

            # rotate the image to deskew it

            (h, w) = parr_original_image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            deskewed_image = cv2.warpAffine(parr_original_image, M, (w,
                    h), flags=cv2.INTER_CUBIC,
                    borderMode=cv2.BORDER_REPLICATE)

            return (deskewed_image, angle)
        except Exception as lobj_exception:
            raise lobj_exception

    def do_correct_alignment(self, pstr_image_path, pobj_logger):
        try:
            now = datetime.now()
            start_time = now.strftime('%Y-%m-%d %H:%M:%S')

            # read and convert the image to grayscale

            larr_image = cv2.imread(pstr_image_path)
            larr_gray_image = cv2.cvtColor(larr_image,
                    cv2.COLOR_BGR2GRAY)
            lstr_base_name = os.path.basename(pstr_image_path)

            (larr_deskewed_image, skew_angle) = \
                self.deskew_images(larr_gray_image, larr_image,
                                   pobj_logger)

            (larr_deskewed_image, rot_angle) = \
                self.rotate_images(larr_deskewed_image, pobj_logger)

            cv2.imwrite(lstr_base_name, larr_deskewed_image)
            now = datetime.now()
            end_time = now.strftime('%Y-%m-%d %H:%M:%S')

            with open(lstr_base_name, 'rb') as original_file:
                deskewed_encoded_string = \
                    base64.b64encode(original_file.read())

            pobj_logger.info('Image Name: ' + pstr_image_path
                             + ' | Skew Degree: ' + str(skew_angle)
                             + ' | Rotation Angle: ' + str(rot_angle)
                             + ' | Start time: ' + start_time
                             + ' | End time: ' + end_time)

            return deskewed_encoded_string
        
        except Exception as  lobj_exception:
            raise lobj_exception
