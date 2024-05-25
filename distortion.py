import requests
import cv2
import numpy as np
import s3
from io import BytesIO

def image_distortion(url, cookie) :
    try :
        origin = requests.get(url[0])
        image = np.asarray(bytearray(origin.content), dtype = np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)

        rows, cols = image.shape[:2]

        exp = 1.1
        scale = 3

        mapy, mapx = np.indices((rows, cols), dtype = np.float32)

        mapx = 2 * mapx / (cols - 1) - 1
        mapy = 2 * mapy / (rows - 1) - 1

        r, theta = cv2.cartToPolar(mapx, mapy)

        r[r < scale] = r[r < scale] ** exp
        mapx, mapy = cv2.polarToCart(r, theta)

        mapx = ((mapx + 1) * cols - 1) / 2
        mapy = ((mapy + 1) * rows - 1) / 2

        distortion_image = cv2.remap(image,mapx,mapy,cv2.INTER_LINEAR)

        bordertop = (rows * 3 - rows) // 2
        borderBottom = (rows * 3 - rows - bordertop)
        borderLeft = (cols * 3 - cols) // 2
        borderRight = (cols * 3 - cols - borderLeft)

        distortion_image = cv2.resize(distortion_image, (cols * 3, rows * 3))
        result_image = cv2.copyMakeBorder(distortion_image, bordertop, borderBottom, borderLeft, borderRight, cv2.BORDER_CONSTANT, value=(0, 0, 0))
        result, result_image = cv2.imencode('.jpg', result_image)

        if (result) :
           S3 = s3.connection_s3()
           return s3.save_image(S3, result_image, cookie, 'distortionPanorama')
        else :
            return False
    
    except Exception as e :
        print(e)
        return False