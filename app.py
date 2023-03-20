from flask import Flask, render_template, request
import requests
import math


# EPA API
# https://data.gov.tw/dataset/34827
api_url = 'https://data.epa.gov.tw/api/v2/aqx_p_02?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate%20desc&format=JSON'
response = requests.get(api_url).json() # To convert JSON strings into a Python dictionary

app = Flask(__name__)

@app.route('/')
def index():
    data = response['records']

    keyword = request.args.get('keyword', '')
    if keyword:
        data = [i for i in data if keyword in i['county'] or keyword in i['site']]

    page = int(request.args.get('page', 1))
    per_page_item = 10
    last_page = math.ceil(len(data) / per_page_item)
    result = []
    for i in range(0, per_page_item):
        idx = (per_page_item * (page - 1)) + i
        try:
            result.append(data[idx])
        except:
            pass
    return render_template('index.html', data=result, keyword=keyword, current_page=page, last_page=last_page)


if __name__=='__main__':
    app.run(debug=True, port=3000)