import re
import datetime
import json
from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.routing import BaseConverter
from config import *


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app = Flask(__name__)
app.url_map.converters['reg'] = RegexConverter
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Chaqiquan(db.Model):
    """
    ORM模型
    """
    __tablename__ = 'cqq_{0}'.format(datetime.datetime.now().strftime('%Y%m%d'))
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), unique=True)
    oneMonth = db.Column(db.Float)
    threeMonth = db.Column(db.Float)
    sixMonth = db.Column(db.Float)

    def __init__(self, code, oneMonth, threeMonth, sixMonth):
        self.code = code
        self.oneMonth = oneMonth
        self.threeMonth = threeMonth
        self.sixMonth = sixMonth

    def __repr__(self):
        return '<Cqq %r>' % self.code


@app.route('/today/')
def today():
    hours = int(datetime.datetime.now().strftime('%H'))
    if hours < 8:
        day = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y%m%d')
    else:
        day = datetime.datetime.now().strftime('%Y%m%d')

    sql = 'SELECT * FROM cqq_' + day + ';'
    result = db.session.execute(
        sql
    )

    # 对象形式
    response = {}
    for i in result:
        response[i.code] = {
            'oneMonth': i.oneMonth,
            'threeMonth': i.threeMonth,
            'sixMonth': i.sixMonth
        }

    # 数组形式
    # response = []
    # for i in result:
    #     item = {
    #         'code': i.code,
    #         'oneMonth': i.oneMonth,
    #         'threeMonth': i.threeMonth,
    #         'sixMonth': i.sixMonth
    #     }
    #     response.append(item)

    return Response(json.dumps(response))


@app.route('/history/<reg("[0-9]{8}"):day>', methods=['GET'])
def history(day):
    sql = 'SELECT * FROM cqq_' + day + ';'
    result = db.session.execute(
        sql
    )

    # 对象形式
    response = {}
    for i in result:
        response[i.code] = {
            'oneMonth': i.oneMonth,
            'threeMonth': i.threeMonth,
            'sixMonth': i.sixMonth
        }

    # 数组形式
    # response = []
    # for i in result:
    #     item = {
    #         'code': i.code,
    #         'oneMonth': i.oneMonth,
    #         'threeMonth': i.threeMonth,
    #         'sixMonth': i.sixMonth
    #     }
    #     response.append(item)

    return Response(json.dumps(response))


@app.route('/inquire/', methods=['GET'])
def inquire():
    form = request.args
    code = form['code']
    if re.match('[0-9]{6}', code):
        result = db.session.query()
        # for i in result:
        #     print(i.oneMonth)
    else:
        result = '代码有误，请重试'
    print(result)
    return Response(str(result))


if __name__ == '__main__':
    app.run()
