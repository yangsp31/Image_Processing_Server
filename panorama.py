import requests
import cv2
import numpy as np
import s3

def create_panorama(urls, cookie) :
    images = []

    try :
        for url in urls :
            image = np.asarray(bytearray(requests.get(url).content), dtype = np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            images.append(image)

        if(len(images) > 1) :
            stitcher = cv2.Stitcher.create()
            result, panorama = stitcher.stitch(images)
        else :
            panorama = images[0]
            result = True
        
        panorama = cv2.resize(panorama, (2048, panorama.shape[0]))
        panorama = cv2.flip(panorama, 1)
        result, image = cv2.imencode('.jpg', panorama)

        if(result) :
            S3 = s3.connection_s3()

            return s3.save_image(S3, image, cookie, 'originPanorama')
        else :
            return False

    except Exception as e :
        print(e)
        return False