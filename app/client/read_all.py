"""app/client/read_all.py
"""

import requests

get_url = '{host}:{port}/feedback/records'.format(**{
    'host': 'http://127.0.0.1',
    'port': '5000'
})

res = requests.get(url=get_url)

print(res.status_code)
print(res.text)
