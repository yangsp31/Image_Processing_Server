from dotenv import load_dotenv
import os
import boto3

load_dotenv()

def connection_s3() :
    s3 = boto3.client('s3',
                      aws_access_key_id = os.environ.get('AWS_S3_ACCESS_KEY'),
                      aws_secret_access_key = os.environ.get('AWS_S3_SECRET_ACCESS_KEY'))
    
    return s3

def save_image(s3, image, cookie, process) :
    s3.put_object(
        Bucket = os.environ.get('AWS_S3_BUCKET_NAME'),
        Body = image.tobytes(),
        Key = cookie + '/panorama/result/' + process + '.jpg',
        ContentType = '.jpg')
    
    return os.environ.get('AWS_S3_OBJECT_URL') + cookie + '/panorama/result/' + process + '.jpg'