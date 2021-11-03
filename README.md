![header](https://capsule-render.vercel.app/api?type=wave&color=auto&height=300&section=header&text=Project%20ISEEU&fontSize=90)

# 🎥생활안전을 위한 스마트CCTV

- ## 💡기능
  * cctv에 감지된 방문자의 얼굴을 인식하여 방문자가 있을시 사용자에게 알림
  * 앱을 이용해 실시간 cctv 영상 제공
  * 등록되지 않은 방문자의 방문시간과 횟수와 통계 제공
  * 주변에서 일어나는 사건 사고 뉴스를 볼 수 있는 서비스
  * 긴급신고 서비스

- ## ✨나의 역할
  * **생활안전정보를 중복없이 제공하기 위한 네이버 기사와 서울안전누리 사이트 크롤링 및 형태소 분석**
  * **밝기의 영향을 줄이기 위한 이미지 Normalization**
  * **CCTV에 인식된 사용자의 얼굴 기울기를 조절하는 Face Alignment**
  * **마스크낀 사용자를 판단하기위한 마스크 오버레이**
  * **실시간 방문자 그래프를 위한 장고 웹페이지 구축**
  * **RDS관리**
  * **학습용 이미지를 위한 얼굴 크롭(opencv,dlib)**
  * **API**
  

- ## 🛠나의 사용 도구
<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white"> <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"> <img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"> <img src="https://img.shields.io/badge/html-E34F26?style=for-the-badge&logo=html5&logoColor=white"> <img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white"> <img src="https://img.shields.io/badge/PyCharm-000000?style=for-the-badge&logo=PyCharm&logoColor=white">
<img src="https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=Selenium&logoColor=white">
<img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=OpenCV&logoColor=white">
<img src="https://img.shields.io/badge/scikit-learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white">
<img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white">
<img src="https://user-images.githubusercontent.com/73850629/139793279-4704c06e-2726-45c6-aa5f-126563656b75.png" height="25px">

- ## 📆개발 기간
  * 2021.4.29 ~ 2021.6.4


</br>

___

## 주제배경

![image](https://user-images.githubusercontent.com/73850629/139790516-fb81643e-a4bb-470a-9ad5-57cd8046c706.png)

2019년 경찰청 범죄 통계에 따르면 
전체 범죄의 26프로가 거주지에서 발생하였고 
절도 범죄의 경우 빈집 절도가 가장 빈번합니다. 통계에 따르면 대부분이 출입문을 통해 침입한다는 것을 알 수 있습니다. 
또한, 전국적으로 1인가구의 수가 증가하는 추세로, 빈집절도나 스토킹 범죄 등에 노출되기 쉬운 1인가구는 특별한 보안 장치가 없는 이상 범죄를 예방하기 어렵습니다. 
특히 최근 일어난 살인사건과 같이 혼자 사는 여성을 대상으로 흉악 범죄로 이어질수 있는 끔찍한 결과를 예방하기 위해 프로젝트 주제로 선정하게 되었습니다.
___
#### 통계

![image](https://user-images.githubusercontent.com/73850629/139790612-e8d1435f-8a6e-404f-9328-d2f4258b1de4.png)
<img src="https://user-images.githubusercontent.com/73850629/139789872-614bbe06-971c-465e-ab9e-4749c9b8072c.png" width="50%"><img src="https://user-images.githubusercontent.com/73850629/139790357-c9bbf83b-ef18-4d05-9393-4bc294095146.png" width="50%">
___



## 서비스 컨셉
![image](https://user-images.githubusercontent.com/73850629/139789719-de0e1a2a-b406-4129-b1a4-1e35a3572297.png)

___
## 시스템 구성도

![image](https://user-images.githubusercontent.com/73850629/139789790-72da8e79-c8b2-442c-83b9-67a0ca76e09e.png)
