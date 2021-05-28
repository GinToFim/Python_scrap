# /usr/bin/env python
# encoding=utf-8


import requests
from bs4 import BeautifulSoup
import telegram
import os
import time

##### 가천대 메인 게시판 스크랩

bot = telegram.Bot(token='1824872114:AAF7Z-s5PFxSdseaACbfVdOouNlDemWy_1s') 
channel_id = -1001259351219 # 채널 ID

# heroku 서버의 환경변수 사용하여 최신글 번호 업데이트
gaMain_lastest_num = os.environ.get('gaMain_ID')

def gaMain() :
    global gaMain_lastest_num

    url = "https://www.gachon.ac.kr/community/opencampus/03.jsp?boardType_seq=358"
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    # table -> tbody -> tr -> td 순서대로 긁음
    data_rows = soup.find("table").find("tbody").find_all("tr")

# 인터프리터에서 최초 실행할 때 조건문 ㄱ
if __name__ == '__main__' :
    last_num = -1 # 제일 최근 게시글 번호 저장

    while True :
        url = "https://www.gachon.ac.kr/community/opencampus/03.jsp?boardType_seq=358"
        res = requests.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")

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
            
            text = '<가천대 게시글 업데이트>' + '\n'
            text += post_num + '\n'
            text += title + '\n'
            text += link

            bot.sendMessage(-1001259351219, text)

            # 터미널 로그
            print(text)