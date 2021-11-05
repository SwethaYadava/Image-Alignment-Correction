# -*- coding: utf-8 -*-
import requests
import json
import base64
import os

lstr_input_image_path = r'misaligned_images\4.jpg'

lstr_output_path = r'aligned_images'

# read the image and convert into base64
with open(lstr_input_image_path, "rb") as original_file:
    encoded_string = base64.b64encode(original_file.read())
    
payload = {'InputImageString':encoded_string.decode('utf-8'),'InputImageName': os.path.basename(lstr_input_image_path)}

url = 'http://localhost:5000/CorrectAlignment'
headers = {'content-type': 'application/json'}
json.dumps(payload)
r = requests.post(url, data=json.dumps(payload), headers=headers)

# get the response from api and conevrt it into json object
ldict_response_data = json.loads(r.text)

# get the deskewed image base64 string and convert it back to image
if 'AlignmentCorrectedImage' in ldict_response_data:
    lstr_deskewed_image = ldict_response_data['AlignmentCorrectedImage']
with open(os.path.join(lstr_output_path,os.path.basename(lstr_input_image_path)), "wb") as new_file:
    new_file.write(base64.decodebytes(bytes(lstr_deskewed_image.encode('utf-8'))))
                
