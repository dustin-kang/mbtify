from flask import Flask, render_template, request
import pickle
import numpy as np
from music import *
from secrets import *

with open('model.pkl','rb') as pickle_file:
   model = pickle.load(pickle_file)

mbtify = Flask(__name__) #어플리케이션 이름 지정

@mbtify.route('/')
def send():
    # root url인 ('/')로 접근 했을 경우 send.html를 렌더링한다.
    return render_template('send.html')


@mbtify.route('/recv', methods=['POST', 'GET']) # 받을 경우
def recv():
    data = request.form['inpute_code']

    info, features = getTrackFeatures(token, data)
    pred = model.predict(features)

    artist = info['artist']
    url = info['image_url']
    song = info['song']
    # 데이터 API 가져와 변환하기
    return render_template('recv.html', pred=pred, artist=artist, url=url, song=song)

@mbtify.errorhandler(404) # 페이지 오류
def page_not_found(error):
    return render_template('404.html'), 404

@mbtify.errorhandler(500) # 페이지 오류
def page_not_found(error):
    return render_template('500.html'), 500

if __name__ == '__main__': # Debug Mode ON
    app.run(debug=True)
