''' s3_service.py - class for interacting with AWS S3 '''
import os
import boto3
from django.conf import settings

class S3Service():
    ''' Class for interacting with AWS S3 '''

    @classmethod
    def upload_file(cls, file_path):
        ''' Uploades the given fully qualified file path to AWS S3 and returns
            the URL of the object '''

        client = boto3.client('s3', settings.AWS_REGION_NAME, 
                              aws_access_key_id=settings.AWS_ACCESS_KEY_ID, 
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

        # throws if file is inaccessible
        file_content = open(file_path, "rb").read()

        file_name = os.path.basename(file_path)

        # delete possible remnant
        client.delete_object(Bucket=settings.AWS_BUCKET_NAME, Key=file_name)

        # perform upload
        client.put_object(Bucket=settings.AWS_BUCKET_NAME, Key=file_name, Body=file_content,
                          ContentType="image", ContentDisposition="inline")

        # return url
        return 'https://' + settings.AWS_BUCKET_NAME + ".s3.amazonaws.com/" + file_name
