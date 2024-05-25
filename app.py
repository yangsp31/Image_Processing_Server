from flask import Flask, request, jsonify
import distortion
import panorama
#from test import match_image

app = Flask(__name__)

@app.route('/Flask/Generate', methods = ['POST'])
def Generate_Panoramic_Image() : 
    data = request.json

    result = panorama.create_panorama(data['fileUrls'], data['cookie'])

    if(result) :
        return jsonify(fileUrl = result), 200
    else :
        return jsonify(message = 'Image stitching error'), 500
    
@app.route('/Flask/Distortion', methods = ['POST'])
def Distortion_Image() :
    data = request.json

    result = distortion.image_distortion(data['fileUrl'], data['cookie'])

    if(result) :
        return jsonify(fileUrl = result), 200
    else :
        return jsonify(message = 'Image distortion error'), 500

if __name__ == '__main__' : 
    app.run(host = '0.0.0.0', port = 5000, debug = True)