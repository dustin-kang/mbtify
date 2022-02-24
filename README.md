# 🎧 Mbtify
Spotify Track을 활용한 MBTI 분류 서비스

<img src="https://user-images.githubusercontent.com/55238671/145755750-c8454f29-a6cd-4ca6-8711-225c83e36277.png" width="500">

## About Mbtify
> Find MBTI using track

Spotify 음원 플랫폼에서 제공하는 MBTI 별 플레이리스트와 곡들을 추출하여 비슷한 성향을 가진 음악적 특징을 활용하여 사용자가 좋아하는 음악의 MBTI를 성향을 예측할 수 있는 서비스이다.

## Data Pipeline
<img src="https://user-images.githubusercontent.com/55238671/145755773-34f3ebdb-45bf-435a-830c-7f255d043e2f.png" width="500">

1. [스포티파이 개발자 홈페이지](https://developer.spotify.com/) 에서 유저들이 만들어낸 플레이리스트의 트랙데이터를 수집합니다.
2. 수집한 데이터들은 `MongoDB`에 적재를 하게 됩니다.
3. 시각화를 위해 적재한 데이터를 LocalDB로 옮기게 됩니다.
4. 이후 `Docker`를 이용해 `Metabase`에서 데이터를 시각화합니다.
5. `Scikit-Learn`을 통해 XGBoost로 모델링을 진행합니다.
6. 마지막으로 `Flask`로 Web 서비스를 구축하고 `Heroku`로 배포 하였습니다.

> 자세한 [Keynote 내용](https://github.com/dustin-kang/Proj3_MusicMBTIClassfication/blob/main/keynote/Keynote.zip)과 [발표 영상](https://www.youtube.com/watch?v=gowY7fZMITE&feature=youtu.be)은 링크를 통해 확인하실 수 있습니다.

## Process
|순번|과정|디렉토리|툴|
|---|---|---|---|
|1|Spotify API를 이용한 데이터 스크레이핑|[Scraping](https://github.com/dustin-kang/Proj3_MusicMBTIClassfication/tree/main/collect/scraping)|Spotify API|
|2|트랙 데이터 적재및 관리|[Collecting](https://github.com/dustin-kang/Proj3_MusicMBTIClassfication/tree/main/collect)|MongoDB, SQLite|
|3|머신러닝 모델링|[Modeling](https://github.com/dustin-kang/Proj3_MusicMBTIClassfication/blob/main/mbtify/modeling.py)|Scikit-Learn|
|4|데이터 분석 및 시각화 |[Visualization](https://github.com/dustin-kang/Proj3_MusicMBTIClassfication/blob/main/keynote/Proj3_keynote/Proj3_keynote.009.png)|Docker, Metabase|
|5|웹 서비스 구현|[Web Service](https://github.com/dustin-kang/Proj3_MusicMBTIClassfication/tree/main/mbtify)|Flask, Heroku|

## Data Schema, flow
<img src="https://github.com/dustin-kang/Proj3_MusicMBTIClassfication/blob/main/keynote/Proj3_keynote/Proj3_keynote.011.png?raw=true" width="300"> <img src="https://github.com/dustin-kang/Proj3_MusicMBTIClassfication/blob/main/keynote/Proj3_keynote/Proj3_keynote.012.png?raw=true" width="300">


## Feed Back
 **데이터 수집부터 데이터베이스 적재, 머신러닝 활용, 웹서비스 개발 및 배포 과정 등 데이터 분야 전과정의 흐름을 간략하게 진행했던 프로젝트** 였다.

## [▶️ 결과 사이트 Mbtify](https://mbtify.herokuapp.com/)

<img src="https://github.com/dustin-kang/Proj3_MusicMBTIClassfication/blob/main/keynote/site_gif.gif?raw=true">
