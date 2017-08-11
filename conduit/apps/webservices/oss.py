import oss2
from rest_framework.exceptions import ValidationError

accessKeyId = "LTAIxuJzCN49WyOx"
accessKeySecret = "YzU2GrECDsYFlePmGeqHAhFYejW5Q8 "
endpoint = "oss-cn-shanghai.aliyuncs.com"
defaultBucketName = "beacon-media"

def upload_to_oss(file_obj, mediaGuid, cameraid, frameid):
    try:
        filename = str.format("%s_%s_%s.jpg" % (mediaGuid, cameraid, frameid))
        # aliyun oss service
        auth = oss2.Auth(accessKeyId, accessKeySecret)
        bucket = oss2.Bucket(auth, endpoint, defaultBucketName)
        bucket.put_object(filename, file_obj)
        print("picture uploaded to oss, filename=%s" % filename)
    except Exception as e:
        raise ValidationError('upload image failed ', e)