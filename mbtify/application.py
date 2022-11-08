# Standard Library imports 

# Third party imports
from flask import Flask, render_template, request
import pandas as pd
import xgboost as xgb

# Local application imports
from crawling_app import gettitleAudioFeatures, token
import pickle

# $ export FLASK_APP=mbtifyapp (환경변수 지정)
# current_app.config['DEBUG'] = True

print('------run------')
application = Flask(__name__)

@application.route('/')
@application.route('/index')
def main():
    # Root URL로 접근하면 main.html 파일로 렌더링한다.
    return render_template('main.html')


@application.route('/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        # 데이터 입력 후 머신러닝 예측하는 작업
        # print(request.form.get('Inputs', False))
        data = request.form['Inputs'] # 포스트 방식으로 값 전달 받기

        df = pd.read_csv('./tracks.csv')
        model = xgb.XGBClassifier() # 모델 초기화
        model.load_model('./xgb.model')
        
        info, features = gettitleAudioFeatures(token, data)
        # print(info)
        pred_data = [list(features.values())]  # 반드시 2차원 데이터
        pred = model.predict(pred_data)
        mbti_list = ['enfj', 'enfp', 'entj' ,'entp','esfj' ,'esfp', 'estj', 'estp' ,'infj', 'infp' ,'intj', 'intp' ,'isfj', 'isfp', 'istj' ,'istp']
        pred = mbti_list[pred[0]]
        print(pred)
        print(pred[0])

        # Mbti 별 노래 추천해주는 서비스
        df_mbti = df[['artist','title','track_id']][df['mbti'] == pred]
        ref_track = df_mbti.sample(n=1).values.tolist()[0] # 리스트로 변경

        # html에 들어갈 변수들
        artist = info['artist']
        url = info['url']
        song = info['title']
        image = info['image']
        ref_url = f'https://open.spotify.com/track/{ref_track[2]}'

        # 데이터 API 가져와 변환하기
        return render_template('recv.html', pred=pred, artist=artist, url=url, song=song, image=image, ref_track = ref_track, ref_url = ref_url)
    
    # 입력없이 url 추가 입력으로 페이지 들어갔을 경우
    if request.method == 'GET' or request.form == None:
        return render_template('search.html')

# 에러 핸들링        
@application.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@application.errorhandler(500)
def server_problem(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    application.debug = True
    # application.run()