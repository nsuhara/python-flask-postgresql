"""app/client/create.py
"""

import json

import requests

post_url = '{host}:{port}/feedback/records'.format(**{
    'host': 'http://127.0.0.1',
    'port': '5000'
})
post_data = json.dumps({
    'service': 'create_service',
    'title': 'create_title',
    'detail': 'create_detail'
})
post_headers = {
    'Content-Type': 'application/json'
}

res = requests.post(url=post_url, data=post_data, headers=post_headers)

print(res.status_code)
print(res.text)
