import pandas as pd
# 1. 데이터 준비하기
df = pd.read_csv('news_comment_BTS.csv')

import re
# 2. 불필요한 문자 제거하기
parse = df['reply'].str.replace('[^가-힣]', ' ', regex=True)

# 3. 명사 추출하기
import konlpy
kkma = konlpy.tag.Kkma()
text_series = parse.apply(kkma.nouns)
text_series
# 단어를 추출한다. (이중 리스트 내포문 사용)
word_list = [ word for li in text_series for word in li ]

# 글자로 데이터 프레임 만들기
df = pd.DataFrame({'word':word_list})

# 글자 길이 2 이상인 데이터만 출력하기
df['len'] = df.word.str.len()
df = df.query('len >= 2')
df.sort_values('len') # len 으로 데이터 정렬하기(낮은 순)

# 4. 데이터 개수 받은 것으로 높은순 정렬하기
df_count = df.word.value_counts(). \
            to_frame().reset_index(). \
            sort_values('word', ascending=False)

# 위에서부터 20개
top20 = df_count.head(20)

# 딕셔너리화 하기 index : 단어, val : 개수
dic_word = df_count.set_index('index').to_dict()['word']

# 패키지 불러오기
from wordcloud import WordCloud
import matplotlib.pyplot as plt
font = "DoHyeon-Regular.ttf"

# 직각 워드 클라우드
# wc = WordCloud(font_path=font, width=400, height=400, background_color='white')
# wordc = wc.generate_from_frequencies(dic_word)
# plt.figure(figsize=(5, 5))
# plt.axis('off')
# plt.imshow(wordc)

# 5. 클라우드 그림화 - 구름모양이미지
import PIL
image = PIL.Image.open('cloud.png')
import numpy as np
img = PIL.Image.new('RGB', image.size, (255, 255, 255))
img.paste(image, image)
img = np.array(img)

# 워드클라우드 객체 만들기
wc = WordCloud(font_path=font,
               width=400,
               height=200,
               mask=img, 
               background_color='white')

# 워드클라우드 객체로 빈도수를 기준으로 한 클라우드 생성
cloud = wc.generate_from_frequencies(dic_word)

# 출력하기 matplotlib 사용
plt.figure(figsize=(5, 5))
plt.axis('off')
plt.imshow(cloud)