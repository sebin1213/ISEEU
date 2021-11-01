import boto3

class SendToS3:
    def __init__(self, bucket):
        self.bucket = bucket
        self.s3 = boto3.client('s3')
    
    def send(self, file_name, key):
        self.s3.upload_file(file_name, self.bucket, key)

if __name__ == '__main__':
    bucket = 'yangjae-team03-s3'
    s = SendToS3(bucket)
    
    file_name = f"./user/6_user_bomi.jpg"
    key = "Registered-User/6_user_bomi.jpg"
    s.send(file_name, key)
