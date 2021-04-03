import requests
import time
import numpy as np
from urllib.parse import urlparse

print('Student ID : 20163079')
print('Name : Dongho Gang')

getKey = 'get '
headers = {
  'User-Agent': 'HW1/1.0'
}

def get_host(url):
  return url.split("//")[-1].split("/")[0].split('?')[0]

def get_raw_request(request):
    request = request.prepare() if isinstance(request, requests.Request) else request
    host = get_host(request.url)
    headers = '\r\n'.join(f'{k}: {v}' for k, v in request.headers.items())
    body = '' if request.body is None else request.body.decode() if isinstance(request.body, bytes) else request.body
    return f'{request.method} {request.path_url} HTTP/1.1\r\nHost: {host}\r\n{headers}\r\n\r\n{body}'

def get(url):
  o = urlparse(url)
  if (o.scheme != 'http'):
    print(f'Only support http, not {o.scheme}')
  else:
    port = (80 if o.scheme == 'http' else 443) if (o.port is None) else o.port
    fileName = url.split('/')[-1]
    try: 
      r = requests.get(url, headers=headers, stream=True)

      raw_request = get_raw_request(r.request)
      print(raw_request)
      
      if (r.status_code == 200):
        file_size = int(r.headers.get('Content-Length', None))
        block_size = 1024
        max_bars = np.ceil(file_size / block_size)
        tenth = 1
        print(f'Total Size {file_size} bytes')
        with open(fileName, 'wb') as f:
          for i, chunk in enumerate(r.iter_content(chunk_size=block_size)):
            f.write(chunk)
            currunt_block_size = i * block_size
            currunt_percent = int(np.around(currunt_block_size / file_size * 100))
            if (currunt_percent > tenth * 10):
              print('Current Downloading', f'({currunt_block_size}/{file_size}) (bytes) {currunt_percent}%')
              tenth += 1
            time.sleep(0.05)
        print(f'Download Complete: {fileName}, {file_size}/{file_size}')
      else:
        print(f'{r.status_code} Not Found')
    except requests.exceptions.RequestException as ce:
      # print('ConnectionError', ce)
      host = get_host(url)
      print(f'{o.scheme} {host} {host} {port} {fileName}')
      print(f'{host}: unknown host')
      print(f'cannot connect to server {host} {port}')
    finally:
      print()

while(True):
  print('> ', end='')
  command = input()
  if (command == 'quit'):
    break
  elif (command.startswith(getKey)):
    url = command.replace(getKey, '', 1)
    get(url)
  else:
    print(f'Wrong command ${command}')