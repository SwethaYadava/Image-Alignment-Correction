# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from logger.APILogger import InvalidUsage
from logger.logger import Logger
from AlignmentCorrection import AlignmentCorrection
import json
import base64

app = Flask(__name__)
app.config["DEBUG"] = True

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

#method to be called to deskew images
@app.route('/CorrectAlignment', methods=['POST', 'GET'])
def home():
    try:
        deskewed_encoded_string = None
        lobj_input_data = json.loads(request.data)
        if lobj_input_data:
            lstr_input_image_path = lobj_input_data['InputImageName']
            lstr_input_image = lobj_input_data['InputImageString']
            
            with open(lstr_input_image_path, "wb") as new_file:
                new_file.write(base64.decodebytes(bytes(lstr_input_image.encode('utf-8'))))
            
            deskewed_encoded_string = gobj_align_images.do_correct_alignment(lstr_input_image_path, gobj_logger)
            return jsonify({"success": True,"AlignmentCorrectedImage":deskewed_encoded_string.decode('utf-8')})
        else:
            gobj_logger.error("Input is None", exc_info=True)
            raise
    except Exception as e:
        print(e)
        gobj_logger.error("Exception Raised", exc_info=True)
        raise InvalidUsage("Error", status_code=500)


if __name__ == '__main__':
    try:

        # ===========================================
        # Create object of a logger
        # ===========================================

        gobj_logger = Logger()
        gobj_logger = gobj_logger.logger

        # =======================================================================
        # create object of AlignmentCorrection
        # =======================================================================
        gobj_align_images = AlignmentCorrection.AlignmentCorrection()

        app.run(host='0.0.0.0',threaded=True)

    except Exception:
        print("ERROR")
        gobj_logger.error("Exception Raised", exc_info=True)
