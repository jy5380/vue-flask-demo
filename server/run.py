from flask import Flask
from flask import request
from flask import make_response
from flask import render_template
from flask_cors import CORS
import sqlite3
import json

app = Flask(__name__)
CORS(app)

def _add_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    response.headers['Content-Type'] = 'application/json'

def _make_res(status, msg, data=None):
    res = {'status': status, 'description': msg, 'content': data}
    response = make_response(_to_json(res))
    _add_cors_header(response)
    return response

def _to_json(res):
    return json.dumps(res, default=lambda obj: obj.__dict__)

@app.route('/check', methods=['GET', 'POST'])
def check():

    conn = sqlite3.connect("I:\\test.db")
    cursor = conn.cursor()
    params = json.loads(request.data)
    name = params['name']
    date1 = params['date1']
    date2 = params['date2']
    cursor.execute('insert into record values(?, ?, ?, ?, ?)', (45, name, date1, date2, 'xxxxxx'))
    # name = request.form['name']
    # date1 = request.form['date1']
    # date2 = request.form['date2']

    print('check from date ' + date1 + 'to date ' + date2)
    
    cursor.execute('select name, date1, date2, loc from record where name=\"' + name + '\" and date1>=\"' + date1 + '\" and date2<=\"' + date2 + '\"')
    res = cursor.fetchall()

    overlap = False
    # for index, item in enumerate(res):
    #     if overlap == True:
    #         break
    #     for index_comp, item_comp in enumerate(res):
    #         if index != index_comp:
    #             if (item[1] >= item_comp[1] and item[1] <= item_comp[2]) or (item[2] >= item_comp[1] and item[1] <= item_comp[2]):
    #                 overlap = True
    #                 # print(item, item_comp)
    #                 break
    #             # print(item, item_comp)
    
    res2 = []
    res3 = []
    for index, item in enumerate(res):
        # if overlap == True:
        #     break
        for item_comp in res[(index+1):]:
            if (item[1] >= item_comp[1] and item[1] <= item_comp[2]) or (item[2] >= item_comp[1] and item[1] <= item_comp[2]):
                res2.append(item)
                res2.append(item_comp)
                overlap = True
            
                # break

    for item in res:
        if item not in res2:
            res3.append(item)
            
    cursor.close()
    conn.close()
    return _make_res('ok', 'msg', res)