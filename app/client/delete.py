"""app/client/delete.py
"""

import requests

delete_url = '{host}:{port}/feedback/records/{record_id}'.format(**{
    'host': 'http://127.0.0.1',
    'port': '5000',
    'record_id': '1'
})

res = requests.delete(delete_url)

print(res.status_code)
print(res.text)
