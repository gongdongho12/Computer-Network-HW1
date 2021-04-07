import socket
import re

carriage_return = '\r\n\r\n'
single_byte = 1
getKey = 'get '

url_regex = re.compile("^((http[s]?|ftp):\/)?\/?([^:\/\s]+)(:([^\/]*))?((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(\?([^#]*))?(#(.*))?$")
header_regex = re.compile("(.*)\: (.*)")
request_regex = re.compile("^HTTP\/\d.\d\s(\d+)\s(.*)")

def get_header(sock):
  data = ''
  header = {}
  status = [404, 'Not Found']
  while True:
    binary = sock.recv(single_byte)
    if(len(binary) < single_byte):
      break
    try:
      data += binary.decode()
      if (data.endswith(carriage_return)):
        headers = header_regex.findall(data)
        for header_data in headers:
          header[header_data[0]] = (header_data[1].replace("\r", "", -1))
        status_data = request_regex.findall(data)[0]
        status = [int(status_data[0]), status_data[1].replace("\r", "", -1)]
        break;
    except Exception as err:
      break
  return header, status

def get_http(url):
  url_data = url_regex.findall(url)[0]
  scheme = url_data[1]
  host = url_data[2]
  if (scheme != 'http'):
    print(f'Only support http, not {scheme}')
  else:
    path = url_data[5]
    port = url_data[4]
    file_name = url_data[7]
    port = int((80 if scheme == 'http' else 443) if (port is None or port == '') else port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
      sock.connect((host, port))
      command = f'GET {path}{file_name} HTTP/1.0'
      print(command)
      command = (f'{command}{carriage_return}').encode()

      sock.send(command)

      header, status = get_header(sock)
      print(f'Host: {host}')
      connection = header['Connection']
      user_agent = 'HW1/1.0'
      print(f'User-agent: {user_agent}')
      print(f'Connection: {connection}')

      if (status[0] == 200):
        file_size = int(header['Content-Length'])
        block_size = 512
        with open(file_name, 'wb') as f:
          currunt_block_size = 0
          tenth = 1
          while (currunt_block_size < file_size):
            currunt_percent = int(round(currunt_block_size / file_size * 100))
            if (currunt_percent > tenth * 10):
              print('Current Downloading', f'({currunt_block_size}/{file_size}) (bytes) {currunt_percent}%')
              tenth += 1
            data = sock.recv(block_size)
            f.write(data)
            currunt_block_size += len(data)
          print(f'Download Complete: {file_name}, {file_size}/{file_size}')
      else:
        print(f'{status[0]} {status[1]}')
    except Exception as err:
      print(f'{scheme} {host} {host} {port} {file_name}')
      print(f'{host}: unknown host')
      print(f'cannot connect to server {host} {port}')
    finally:
      sock.close()
  print()

print('Student ID : 20163079')
print('Name : Dongho Gang', end=carriage_return)
while(True):
  print('> ', end='')
  command = input()
  if (command == 'quit'):
    break
  elif (command.startswith(getKey)):
    url = command.replace(getKey, '', 1)
    get_http(url)
  else:
    print(f'Wrong command {command}')