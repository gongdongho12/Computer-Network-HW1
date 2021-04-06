import http.client
from urllib.parse import urlparse
import math

print('Student ID : 20163079')
print('Name : Dongho Gang')

getKey = 'get '
headers = {
  'User-Agent': 'HW1/1.0',
  'Connection': 'Keep-Alive'
}

def get(url):
  o = urlparse(url)
  scheme = o.scheme
  if (scheme != 'http'):
    print(f'Only support http, not {scheme}')
  else:
    host = o.hostname
    fileName = url.split('/')[-1]
    conn = http.client.HTTPConnection(host)
    payload = ''
    path_url = o.path
    port = conn.port if conn.port else conn.default_port
    try:
      conn.request("GET", path_url, payload, headers)
      res = conn.getresponse()

      header_text = '\r\n'.join(f'{k}: {v}' for k, v in headers.items())
      print(f'{conn._method} {path_url} {conn._http_vsn_str}\r\nHost: {host}\r\n{header_text}')
      print()

      status = res.status
      if (status == 200):
        file_size = int(res.getheader('Content-Length'))
        block_size = 512
        with open(fileName, 'wb') as f:
          currunt_block_size = 0
          tenth = 1
          while (not res.closed and currunt_block_size < file_size):
            currunt_percent = int(round(currunt_block_size / file_size * 100))
            if (currunt_percent > tenth * 10):
              print('Current Downloading', f'({currunt_block_size}/{file_size}) (bytes) {currunt_percent}%')
              tenth += 1
            data = res.read(block_size)
            f.write(data)
            currunt_block_size += block_size
          print(f'Download Complete: {fileName}, {file_size}/{file_size}')
      else:
        print(f'{status} Not Found')
    except Exception as e:
      print(f'{scheme} {host} {host} {port} {fileName}')
      print(f'{host}: unknown host')
      print(f'cannot connect to server {host} {port}')
    finally:
      print()
  # print(data)

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