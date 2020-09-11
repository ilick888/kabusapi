from flask import Flask, session
import urllib.request
import json
import pprint

app = Flask(__name__)
app.secret_key = "hoge"

#トークンを取得し、セッションに保持する
@app.route('/api/token/<string:password>')
def token(password):
    obj = { 'APIPassword': password }
    json_data = json.dumps(obj).encode('utf8')
    url = 'http://localhost:18080/kabusapi/token'
    req = urllib.request.Request(url, json_data, method='POST')
    req.add_header('Content-Type', 'application/json')

    try:
        with urllib.request.urlopen(req) as res:
            print(res.status, res.reason)
            for header in res.getheaders():
                print(header)
            print()
            content = json.loads(res.read())
            session['token'] = content
            return content
    except urllib.error.HTTPError as e:
        print(e)
        content = json.loads(e.read())
        return content
    except Exception as e:
        print(e)

#東証銘柄の株価情報を取得
@app.route('/api/board/<int:code>')
def board(code):
    url = 'http://localhost:18080/kabusapi/board/{}@1'.format(code)
    req = urllib.request.Request(url, method='GET')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-KEY', session['token'].get('Token'))

    try:
        with urllib.request.urlopen(req) as res:
            print(res.status, res.reason)
            for header in res.getheaders():
                print(header)
            print()
            content = json.loads(res.read())
            return content
    except urllib.error.HTTPError as e:
        print(e)
        content = json.loads(e.read())
        return content
    except Exception as e:
        print(e)

@app.route('/')
def hello():
    return session['token'].get('Token')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)