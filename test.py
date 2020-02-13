from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


## HTML을 주는 부분
@app.route('/')
def test():
    return render_template('new.html')


## API 역할을 하는 부분
@app.route('/post', methods=['POST'])
def post():
    # value = request.form['test']
    # print(value)
    # return value
    # URL을 읽어서 HTML를 받아오고,
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://www.daum.net/', headers=headers)

    # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
    soup = BeautifulSoup(data.text, 'html.parser')

    # select를 이용해서, 상위 테그정보들을 불러오기
    keywords = soup.select('#mArticle > div.cmain_tmp > div.section_media > div.hotissue_builtin > div.realtime_part > ol > li')
    list_daum = []
    for keyword in keywords:
        # print(keyword.find('span', class_="txt_issue").text)
        list_daum.append(keyword.find("span", class_="txt_issue").text)
    return render_template('post.html', abc=list_daum)

if __name__ == '__main__':
    app.run('localhost', port=7000, debug=True)
