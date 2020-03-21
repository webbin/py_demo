
from urllib import request
import requests
from io import open
import os

bundle_url = 'http://localhost:8081/index.js.bundle?platform=ios&dev=true&minify=false'

data = requests.get(bundle_url)
bundle_file = open('./bundle.txt', 'wb+')

# print(len(texts))
bundle_bytes = bytes(data.text, 'utf-8')
bundle_file.write(bundle_bytes)
print('write bundle done')
os.popen('subl ./bundle.txt')
