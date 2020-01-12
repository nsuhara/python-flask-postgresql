"""app/client/read_one.py
"""

import requests

get_url = '{host}:{port}/feedback/records/{record_id}'.format(**{
    'host': 'http://127.0.0.1',
    'port': '5000',
    'record_id': '1'
})

res = requests.get(url=get_url)

print(res.status_code)
print(res.text)
