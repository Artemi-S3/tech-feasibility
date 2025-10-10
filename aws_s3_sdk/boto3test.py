import boto3
import io
import time

s3 = boto3.client("s3")

# list buckets
print([b["Name"] for b in s3.list_buckets()["Buckets"]])

bucket = "my-bucket"
key = "folder/helloworld.txt"

# upload string
s3.put_object(Bucket=bucket, Key=key, Body=b"hello world")

# download to memory
obj = s3.get_object(Bucket=bucket, Key=key)
data = obj["Body"].read()
print(data.decode())

# upload from file
s3.upload_file("local.txt", bucket, "texts/local.txt")

# download to file
s3.download_file(bucket, key, "hello_world_download.txt")

# presigned URL
url = s3.generate_presigned_url("get_object", 
                                Params={"Bucket": bucket, "Key": key}, 
                                ExpiresIn=300)
print(url)
