import os
import cv2
from keras import preprocessing
from keras import backend as K
from keras.models import load_model
import tensorflow as tf
import numpy as np
import warnings

class IseeUAI:
    def __init__(self):
        # 모델 로드
        # 경로 라즈베리파이 환경에 맞게바꿔야함

        # self.model = load_model('./korean400_batch32_0.847.h5',
        #                         custom_objects={'contrastive_loss': self.contrastive_loss,
        #                                         'euclidean_distance': self.euclidean_distance})

        self.model = load_model('./MC_project_final_100_84.294%.h5',
                                custom_objects={'contrastive_loss': self.contrastive_loss,
                                                'euclidean_distance': self.euclidean_distance})
        
        print('\n모델 로드 완료\n')
        
        self.user_img = []
        self.user_dict = {}

        self.unknown_img = []
        self.unknown_dict = {}

        self.crop_img = []
        self.crop_dict = {}

        self.result_list = []

        self.threshold = 0.4

        self.user_face_path = './user'
        self.unknown_face_path = './unknown'
        self.crop_face_path = './crop'

        self.make_person_list(self.user_face_path, 'user')
        
        warnings.filterwarnings('ignore')

    # user 와 unknown 각각 한번씩 실행시켜 줘야 함 (혹은 업데이트 시에 한번 더)
    def make_person_list(self, face_path, target):
        img_paths = self.get_image_path(face_path)

        for idx, path in enumerate(img_paths):

            img = self.image_processing(path)

            # target으로 user/unknown/crop 구분
            if target == 'user':

                # self.user_dict = {}
                # self.user_img = []

                self.user_dict[idx] = path
                self.user_img.append(img)
            elif target == 'unknown':

                # self.unknown_dict = {}
                # self.unknown_img = []

                self.unknown_dict[idx] = path
                self.unknown_img.append(img)
            else:

                # self.crop_dict = {}
                # self.crop_img = []

                self.crop_dict[idx] = path
                self.crop_img.append(img)

    def predict(self, target):
        if target == 'user':
            person_img = self.user_img
        else:
            person_img = self.unknown_img

        # 비교 대상이 없을 때 (unknown에 아무도 없을 때를 위한 것)
        if len(person_img) == 0:
            ## 원본 코드
            # return False
            ## 수정 코드 : new_unknown_image_record_write() 함수 실행 시킬 수 있는 값 리턴
            return (target, -1)

        self.result_list = []

        for num in range(len(person_img)):

            pred_result = []

            for img in self.crop_img:
                pred_result.append(self.model.predict([img, person_img[num]])[0][0])

            result = self.make_result(pred_result, target)
            self.result_list.append(result)

        print(self.result_list)
        min_value = min(self.result_list, key= lambda x: x[0]) # 수정 코드 : min_value는 리스트(result)
        person_id = self.result_list.index(min_value)
        # temp, person_gender = min_value[2].split('_')
        # person_gender = person_gender.split('.')[0]

        # 수정 코드 : min_value는 리스트이므로 thershold와 비교하는 것은 min_value[0] => 즉 가장 낮은 평균값
        # print("비교 : ", min_value[0], self.threshold)

        # print(f"측정 값 {min_value[0]} , 기준값 {self.threshold}")
        if min_value[0] <= self.threshold:
            return (target, person_id)
        else: # threshold 를 모두 넘지 못했을 때
            return (target, -1)

    def image_record_write(self, target, person_id, time):
        save_image = cv2.imread(self.result_list[person_id][2])

        # print(self.result_list[person_id][2])
        # temp1, temp2, gender = self.result_list[person_id][2].split('_')
        # gender = gender.split('.')[0]
        print(f"{person_id+1}_{target}로 판별됨")
        file_name = f"./record/{target}_{person_id+1}_{time}.jpg"
        cv2.imwrite(file_name, save_image)
        # 문제점 : 기록이 겹처서 사진이 덮어쓰기 됨. 시간 정보를 받아서 저장해야 함
        # 그리고 boto3로 클라우드에 올려줘야 함
        return f"{target}_{person_id+1}_{time}.jpg"

    def new_unknown_image_record_write(self, time):
        save_image = cv2.imread(self.crop_dict[0])
        # gender = self.crop_dict[0].split('.jpg')[0]
        # print('---------------------------', self.crop_dict[0], '---------------------------',)
        # temp, gender = self.crop_dict[0].split('_')
        # gender = gender.split('.')[0]

        file_name_for_face = f"./unknown/{len(self.unknown_img)+1}_unknown.jpg"
        file_name_for_record = f"./record/unknown_{len(self.unknown_img)+1}_{time}.jpg"
        ## 수정 코드 필요 : file_name_for_face 동작이 안됨 !! => unknown 폴더에 이미지 저장 안됨, record는 저장됨

        cv2.imwrite(file_name_for_face, save_image)
        cv2.imwrite(file_name_for_record, save_image)

        print('새로운 사람 등장! Unknown에 등록 : ', f"{len(self.unknown_img)+1}_unknown")
        return (f"{len(self.unknown_img)+1}_unknown.jpg", f"unknown_{len(self.unknown_img)+1}_{time}.jpg")

    # 모델 관련 설정
    def contrastive_loss(self, Y_true, D):
        Y_true= tf.cast (Y_true, tf.float32)
        margin = 1

        return K.mean(Y_true * K.square(D) + (1 - Y_true) * K.maximum((margin-D),0))

    def euclidean_distance(self, vectors):
        vector1, vector2 = vectors
        sum_square = K.sum(K.square(vector1 - vector2), axis=1, keepdims=True)

        return K.sqrt(K.maximum(sum_square, K.epsilon()))

    # 경로 내 사진 리스트화
    def get_image_path(self, path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        imagePaths.sort()

        return imagePaths

    # 이미지 처리
    def image_processing(self, image):
        img = preprocessing.image.load_img(image, color_mode = "grayscale")
        # img = preprocessing.image.load_img(image, color_mode = "rgb")
        img = preprocessing.image.img_to_array(img).astype('float32') / 255
        img = cv2.resize(img, (100, 100))  # 사진 봐서 바꿔야함
        img = img.reshape(img.shape[0], img.shape[1], 1)
        img = np.expand_dims(img, axis=0)

        return img

    # 결과 도출
    def make_result(self, pred_list, target):
        pred_mean = sum(pred_list)/len(pred_list)
        pred_min = min(pred_list)

        pred_min_img_index = pred_list.index(pred_min)  # 유사도 가장 높은 이미지 선택

        ## 원본 코드
        # if target == 'user':
        #     result = [pred_mean, pred_min, self.crop_dict[pred_min_img_index]]
        # else: # unknown
        #     result = [pred_mean, pred_min, self.unknown_dict[pred_min_img_index]]
        #
        # return result

        ## 수정 코드
        result = [pred_mean, pred_min, self.crop_dict[pred_min_img_index]]

        # self.crop_dict = {}
        # self.crop_img = []

        # self.unknown_dict = {}
        # self.unknown_img = []

        return result
