import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb

# 데이터 전처리
df = pd.read_csv('data/mbti/tracks.csv')

# df['mbti'] = df['mbti'].str.lower() # mbti 소문자 대문자 처리
# df['loudness'] += 30 # 정수 조절을 위해 30를 추가 (최소값이 -29이므로 조절을 위함)
# df.to_csv('data/mbti/tracks.csv', index=False)


# 머신러닝 모델링
def modeling(df):
    """
    머신러닝 모델링
    - `sklearn` `xgboost` 설치
    - minMaxScaler를 활용해 서로 다른 features의 크기를 통일 시킨다.
    - XGB 분류 알고리즘을 이용하여 데이터를 분류한다.
    
    - 리턴 값 : model
    - 파라미터 : 데이터프레임
    """
    target = "mbti" # mbti를 타겟값으로 설정
    
    df_info = df[df.columns[0:3]] # data에 대해 모델링용도로 쓰이지 않을 정보
    y = df['mbti'] # label
    X = df[df.columns[4:-1]] # data

    minmax_scaler = MinMaxScaler()
    minmax_scaler.fit(X)
    X_scaled = minmax_scaler.transform(X)
    ## DataFrame으로 전환
    output = pd.DataFrame(X_scaled, columns=X.columns, index=list(X.index.values))

    le = LabelEncoder()
    y = le.fit_transform(y)

    model = xgb.XGBClassifier()
    model = model.fit(output, y) # 학습

    return model, minmax_scaler,le

model, scaler, le = modeling(df)

model.save_model('modeling/xgb.model')