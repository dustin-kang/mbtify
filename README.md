# 🎧 음악을 통해 MBTI 성향을 예측하고 추천하는 MBTIfy

<a href="http://mbtify.eba-9m3ee2dq.ap-northeast-2.elasticbeanstalk.com"><img src="https://github.com/dustin-kang/db-music-mbti-classification/blob/main/keynote/title2.png?raw=true" width="1000" height="300"></a>

👆 클릭 시 해당 서비스를 이용할 수 있습니다.[📱서비스 이용 방법](https://youtube.com/shorts/OBD342fP8Pk?feature=share)

## 🎵 Find Your Music for ME.
신박한 발상으로 시작된 프로젝트로 다양한 분위기와 장르가 있는 **음악이 MBTI와 비슷한 연관성을 가지지 않을까**라는 생각을 시작으로 이를 통해 **음악을 추천**해주는 서비스로 생각을 이어갔습니다.

## 🎵 MBTIfy Process



### 🔷 음원 DB 구축
- 이 프로젝트에서 사용할 음원 데이터는 [**Spotify Developer 사이트**](https://developer.spotify.com/)에서 제공하는 MBTI **플레이리스트들 기반으로 API를 크롤링**하였습니다.
  >  💡 지난 버전의 데이터 부족을 해결하기 위해 4000곡의 음원 데이터로 정확도를 높혔습니다.

- 버전 1에서는 추가적인 데이터 분석 **시각화를 위해 SQLite를 사용**하여 분석을 진행하였으나 이번에는 CSV 파일로 저장하였습니다.
- 기존 API를 통해 JSON 파일에서 분석, 모델링에 필요한 Features 만 가공하여 정제된 데이터로 저장하였습니다. 

### 🔷 데이터 분석 시각화
<center><img src="https://github.com/dustin-kang/db-music-mbti-classification/blob/main/keynote/EDA%20Dashboard.png?raw=true" width="800"> </center>
  
- 감정형, 사고형의 따라 장조와 단조간 차이가 있다는 것을 발견했습니다.
- 내향형일 수록 어쿠스틱함을 선호하는 것으로 보입니다.
- 긍정적 척도는 보통 외향성이 많았으며, 그 중 ESTP가 가장 높았습니다.
- 데이터 시각화 대시보드는 Metabase 툴을 통해 시각화 하였습니다.

### 🔷 머신러닝 모델링
- 지도 학습 중 **XGBoost Classifier 모델을 활용**하여 데이터를 학습하여 분류하였습니다.
- 데이터의 특성들(features)의 **수치적 균형을 맞추기 위해 MinMaxScaler를 사용**하였습니다.
- 사용자가 음원을 입력하면 모델을 통해 예측하고 **이 성향에 맞는 음원을 랜덤으로 추천**해주는 서비스 입니다.
> 💡 버전 2부터 음원을 추천해주는 서비스를 도입하였습니다.

### 🔷 Flask 웹 개발 및 AWS EB 서버
- Flask 웹 개발 프레임워크를 사용하여 **웹 서비스를 개발**하였습니다.
- 사용자가 input에 입력하면 POST 프토토콜을 통해 result 페이지에 출력하게됩니다.
- AWS EB를 이용하여 **웹 어플리케이션을 배포**하고 도메인 등록으로 사용자에게 간편한 플랫폼을 제공합니다.
> 💡 버전 1에서는 Heroku를 사용하였고 버전 2에서는 시험삼아 AWS EB를 사용해봤습니다.

> 💡 [Heroku 대신 AWS를 사용한 이유](https://github.com/dustin-kang/db-music-mbti-classification/issues/16#issue-1434680476)


## 🎵 Requirements & File Tree
- python 3.8
- scikit-learn 1.1.3
- flask 2.2.2
- pandas 1.5.1
- requests 2.28.1
- xgboost 1.7.0
- awsebcli 3.20.3

```py
├── README.md # README 
├── keynote # 버전 1 발표 자료
└── mbtify 
    ├── application.py # 웹 서비스 실행 파일
    ├── crawling_app.py # 데이터 크롤링 및 API 실행 파일
    ├── requirements.txt # 버전 관리
    ├── screts_key.py # 비밀 키
    ├── static # 이미지 파일 및 디자인 파일
    │   ├── css
    │   │   ├── bootstrap.min.css
    │   │   └── main.css
    │   └── img
    │       └── logo.png
    ├── templates # 페이지 html 파일
    │   ├── 404.html
    │   ├── 500.html
    │   ├── main.html
    │   ├── recv.html
    │   └── search.html
    ├── tracks.csv # 데이터 파일
    └── xgb.model # 머신러닝 모델
```

## 🎵 Git Flow
<img src="https://github.com/dustin-kang/db-music-mbti-classification/blob/main/keynote/gitflow.png?raw=true" width="1000" height="300">

- main : 테스트가 끝나고 운영서버로 배포할 수 있는 브랜치
- engine : ETL 작업 및 머신러닝 모델링을 담당하는 브랜치
- develop : 테스트 전 웹 기능 개발을 담당하는 브랜치
- release : 출시전 배포 시험 후 테스팅을 하는 브랜치

##  🎵 성과 및 관련 사이트

|결과 사이트|키노트 자료|발표 영상|배포 후 이슈|
|---|---|---|---|
|<a href="http://www.mbtify.ml"><img src="https://github.com/dustin-kang/db-music-mbti-classification/blob/main/mbtify/static/img/logo.png?raw=true" width="150"></a>|<a href="https://github.com/dustin-kang/Proj3_MusicMBTIClassfication/blob/main/keynote/Keynote.zip"><img src="https://help.apple.com/assets/62E31B0DCD51FF6A7744DA41/62E31B10CD51FF6A7744DA65/ko_KR/9f4f29146401b66b0d7a0668c3345ff4.png" width="150"></a>|<a href="https://www.youtube.com/watch?v=gowY7fZMITE&feature=youtu.be"><img src="https://cdn-icons-png.flaticon.com/512/1384/1384060.png" width="150"></a>|<a href="https://github.com/dustin-kang/db-music-mbti-classification/issues/17"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Commons-emblem-issue.svg/768px-Commons-emblem-issue.svg.png" width="150"></a>|


- 데이터 수집부터 데이터베이스 적재, 머신러닝 활용, 웹서비스 개발 및 배포 과정 등 데이터 분야 전과정의 흐름을 간략하게 진행했던 프로젝트였다.
- 버전 1, 버전 2에서도 급격한 트래픽 증가로 서버에 문제가 발생하는 것은 아직 해결되지 못했다. 추후 이슈에 적어놓고 차근차근 해결해 나갈 예정이다.


<br>
<br>
<br>
<br>

<center> @2021 dustin single project </center>
