import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.

# URL을 읽어서 HTML를 받아오고,
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
url = 'https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20170304'
data = requests.get(url, headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')

# select를 이용해서, tr들을 불러오기
musics = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

# musics (tr들) 의 반복문을 돌리기
for music in musics:
    rank = music.select_one('td.number').text.split()[0]
    image = music.select_one('img').attrs['src'].replace('//', '')
    title = music.select_one('td.info > a.title').text.strip()
    artist = music.select_one('td.info > a.artist ').text
    print(rank,image,title,artist)
    music_data = {
        'rank': rank,
        'image': image,
        'title': title,
        'artist': artist
    }
    db.musics.insert_one(music_data)
