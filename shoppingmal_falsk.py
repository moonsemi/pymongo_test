from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.

app = Flask(__name__)


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('shopping-mall.html')


## API 역할을 하는 부분
# 주문보기 API
@app.route('/order', methods=['GET'])
def orders_view():
    # 서버 내부에서 수행 할 기능 / DB에 저장돼있는 모든 (이름, 수량, 주소, 휴대폰번호) 정보를 가져오기
    all_orders = list(db.orders.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'all_orders': all_orders})


# 주문하기 API
@app.route('/order', methods=['POST'])
def orders_save():
    # 요청할 때 함께 줄 데이터
    name_receive = request.form['name_give']
    count_receive = request.form['count_give']
    addr_receive = request.form['addr_give']
    tel_receive = request.form['tel_give']

    # 서버 내부에서 수행 할 기능 / mongoDB에 넣는 부분
    order = {
        'name': name_receive,
        'count': count_receive,
        'addr': addr_receive,
        'tel': tel_receive,
    }
    db.orders.insert_one(order)

    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)
