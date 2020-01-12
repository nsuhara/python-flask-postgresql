"""app/client/update.py
"""

import json

import requests

update_url = '{host}:{port}/feedback/records/{record_id}'.format(**{
    'host': 'http://127.0.0.1',
    'port': '5000',
    'record_id': '1'
})
update_data = json.dumps({
    'service': 'update_service',
    'title': 'update_title',
    'detail': 'update_detail'
})
update_headers = {
    'Content-Type': 'application/json'
}

res = requests.put(url=update_url, data=update_data, headers=update_headers)

print(res.status_code)
print(res.text)
