import json
import requests
import base64
from flask import Flask, render_template
from flask_restful import request, abort

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    lon = None
    lat = None
    data = request.json
    keyword = data['keyword']
    with open('citys.json', 'r', encoding='UTF-8') as f:
        china_citys = json.load(f)

        for e in china_citys:
            if keyword == e['name']:
                lon = e['log']
                lat = e['lat']
                break
    
    if lon is None or lat is None:
        with open('images/404.png', 'rb') as im:
            im_404 = str(base64.b64encode(im.read()), 'utf-8')
        return {'base64Image':im_404, 'code':404}, 200
        
    weathr_url = f'https://www.7timer.info/bin/civillight.php?lon={lon}&lat={lat}&lang=zh-CN&ac=0&unit=metric&tzshift=1'
    payload={}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}

    response = requests.request('GET', weathr_url, headers=headers, data=payload)
    img = str(base64.b64encode(response.content), 'utf-8')
    res_dict = {'base64Image':img, 'code':200}
    return res_dict


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context='adhoc')