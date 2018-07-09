import boto3
import os


def s3PdfAccess(url,target_path):
  s3_client = boto3.client('s3')
  bucket, key = url.split('/',0)[-1].split('/',1)
  fname = key.rsplit('/',1)[1]
  s3_client.download_file(bucket, key, target_path + '/' + fname)
  return fname