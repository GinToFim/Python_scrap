# /usr/bin/env python
# encoding=utf-8
##### 가천대 메인 게시판 스크랩 #####

import os
import requests
from bs4 import BeautifulSoup
import telegram

# 텔레그램 관련 코드 
myToken = '1824872114:AAF7Z-s5PFxSdseaACbfVdOouNlDemWy_1s' #  Token_key
# channel_id = -1001259351219 # Channel_id
chat_id = 1854365300    # Chat_id

bot = telegram.Bot(token=myToken) 

url = "https://www.gachon.ac.kr/community/opencampus/03.jsp?boardType_seq=358"
res = requests.get(url)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")

# heroku 서버의 환경변수를 사용하여 최신글 번호 업데이트
# last_save_num = os.environ.get('MAIN_POST_ID')
# 게시글 번호 저장 (문자열로 저장 주의 & 일단 임의의 숫자)
last_save_num = '9643'

# table -> tbody -> tr -> td 순서대로 긁음
last_post = soup.find("table").find("tbody").find("tr")
last_post_num = last_post.find("td").get_text()

# last_post_num이 그림이면 == ''(빈문자열) 반복 / 숫자일 때 멈춤 
while (last_post_num == '') :
    last_post = last_post.find_next_sibling()   # 다음 게시물 찾기
    last_post_num = last_post.find("td").get_text()

if(last_save_num == last_post_num) :
    print("최근 게시물 이미 출력")
else :
    # table -> tbody -> tr -> td 순서대로 긁음
    data_rows = soup.find("table").find("tbody").find_all("tr")
    for row in data_rows :
        columns = row.find_all("td")

        # tr 태그 안에 td 가 하나 이하인 데이터는 skip
        if len(columns) <= 1 :
            continue

        link = 'https://www.gachon.ac.kr/community/opencampus/'
        post_num = columns[0].get_text().strip()
        title = columns[1].get_text().strip()
        link += columns[1].find('a').attrs['href']
        
        # 만약 post_num 이 빈 문자열이면 뛰어넘기(image 파일)
        if(post_num == '') :
            continue
        
        # 새로운 글 이미지 태그가 없으면 뛰어 넘기
        new_post = columns[1].find('img')
        if new_post == None :
            continue

        text = '<가천대 게시글 업데이트>' + '\n'
        text += post_num + '\n'
        text += title + '\n'
        text += link

        bot.sendMessage(chat_id, text)

        # 터미널 로그
        print(text)