from flask import Flask, render_template, request
app = Flask(__name__) #어플리케이션 이름 지정

@app.route('/')
@app.route('/index') # 보낼 경우
def from_send():
    # root url인 ('/')로 접근 했을 경우 send.html를 렌더링한다.
    return render_template('send.html')


# @app.route('/form_send') 
# def form_send():
#     return render_template('form_send.html')

@app.route('/form_recv', methods=['POST', 'GET']) # 받을 경우
def from_recv():
    # '/from_recv'로 접근 했을 때, form 데이터는 request 객체를 이용해 전달 받고
    # recv.html 렌더링 하면서 넘겨준다.
    if request.method == "POST": 
        input_type = request.form
        # input type에 대한 함수 넣기 : https://roksf0130.tistory.com/100
        return render_template("recv.html", input_type = input_type)
    else :
        input_type = {}

@app.errorhandler(404) # 페이지 오류
def page_not_found(error):
    return render_template('page_not_found.html'), 404



if __name__ == '__main__': # Debug Mode ON
    app.run(debug=True)
