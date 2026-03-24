import urllib.request, urllib.error, json

def get_dataset():
    url = 'http://127.0.0.1:5000/api/dataset'
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            print('GET', url, '->', r.status, r.getheader('Content-Type'))
            data = r.read(200000)
            try:
                j = json.loads(data.decode('utf-8'))
                print('items:', len(j) if isinstance(j, list) else 'not-list')
            except Exception as e:
                print('could not parse json:', e)
    except Exception as e:
        print('GET failed', e)


def post_chat(msg='hello'):
    url = 'http://127.0.0.1:5000/api/chat'
    try:
        req = urllib.request.Request(url, data=json.dumps({'message':msg}).encode('utf-8'), headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(req, timeout=5) as r:
            print('POST', url, '->', r.status, r.getheader('Content-Type'))
            print(r.read().decode('utf-8'))
    except Exception as e:
        print('POST failed ->', e)

if __name__ == '__main__':
    get_dataset()
    post_chat('how to open a savings account?')
