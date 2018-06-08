from app import db
import app
import time
import json
import random
import requests


headers = {
    'Referer': 'http://www.chaqiquan.com/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15'
}

data = {
    'industry': '',
    'moneySum': '',
    'classify': None,
    'order': ''
}

db.create_all()

result = []
for i in range(100):
    data['pageNo'] = i + 1
    response = json.loads(requests.post(headers['Referer'] + 'api/otcOptions/tradeOtcSearch', data=data, headers=headers).text)

    for i in response:
        result.append({
            'code': i['subjectCode'],
            'oneMonth': i['american1MonthUpPrice'],
            'threeMonth': i['american3MonthUpPrice'],
            'sixMonth': i['american6MonthUpPrice']
        })

    time.sleep(random.randint(3, 5))

print(result)

db.session.execute(
    app.Chaqiquan.__table__.insert(),
    result
)
db.session.commit()
