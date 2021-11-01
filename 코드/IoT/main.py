from iseeu_ai import IseeUAI
# from detect_face import DetectFace
import datetime
import boto3

bucket = 'yangjae-team03-s3'
s3 = boto3.client('s3')

load_model_start_time = datetime.datetime.now()
i = IseeUAI()
load_model_end_time = datetime.datetime.now()

print("\n모델 로드하는데 걸리는 시간 : ", load_model_end_time-load_model_start_time)

# user_face_path = './user'
# unknown_face_path = './unknown'
# crop_face_path = './crop'

# i.make_person_list(user_face_path, 'user')

def main():
    global i
    global s3
    global bucket

    for _ in range(3):
        i.make_person_list(i.unknown_face_path, 'unknown')

        time = datetime.datetime.now()
        time = time.strftime("%Y%m%d_%H%M%S")

        print('시작시간 : ', time)

        # c = DetectFace()
        # c.run()

        i.make_person_list(i.crop_face_path, 'crop')

        print("\n------------예측 시작 (user)-----------")
        predict_start_time = datetime.datetime.now()

        target, person_id = i.predict('user')
        predict_end_time = datetime.datetime.now()
        print("------------예측 완료 (user)-----------")

        print("\n예측하는데 걸린 시간 (user) : ", predict_end_time-predict_start_time)

        if person_id != -1:
            key = i.image_record_write(target, person_id, time)

            file_name = f"./record/{key}"
            key = 'IO-Record/' + key
            res = s3.upload_file(file_name, bucket, key)

        else:
            print("\n------------예측 시작 (unknown)-----------")
            predict_start_time = datetime.datetime.now()

            target, person_id = i.predict('unknown')
            predict_end_time = datetime.datetime.now()
            print("------------예측 완료 (unknown)-----------")

            print("\n예측하는데 걸린 시간 (unknown) : ", predict_end_time-predict_start_time)

            if person_id != -1:
                key = i.image_record_write(target, person_id, time)

                file_name = f"./record/{key}"
                key = 'IO-Record/' + key
                res = s3.upload_file(file_name, bucket, key)

            else:
                key_unknown, key_record = i.new_unknown_image_record_write(time)

                file_name = f"./unknown/{key_unknown}"
                key_unknown = 'UnRegistered-User/' + key_unknown
                res = s3.upload_file(file_name, bucket, key_unknown)

                file_name = f"./record/{key_record}"
                key_record = 'IO-Record/' + key_record
                res = s3.upload_file(file_name, bucket, key_record)
        
        
        i.crop_dict = {}
        i.crop_img = []

        i.unknown_dict = {}
        i.unknown_img = []



main()