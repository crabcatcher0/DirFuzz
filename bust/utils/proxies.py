# ip = 51.38.177.96
# port = 7497

import requests

proxy = {"http": "http://103.167.135.111:80", "https": "http://116.98.229.237:10003"}

req = requests.get("http://127.0.0.1:8000", proxies=proxy)
print(req)
