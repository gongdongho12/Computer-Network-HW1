import socket
import re

carriage_return = '\r\n\r\n'
single_byte = 1
url_regex = re.compile("^((http[s]?|ftp):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.*)?(#[\w\-]+)?$")
header_regex = re.compile("(.*)\: (.*)")

def get_header(sock):
  data = ''
  header = {}
  while True:
    binary = sock.recv(single_byte)
    if(len(binary) < single_byte):
      break
    try:
      data += binary.decode()
      if (data.endswith(carriage_return)):
        headers = header_regex.findall(data)
        for header_data in headers:
          print(f'{header_data[0]} : {header_data[1]}')
          header[header_data[0]] = (header_data[1].replace("\r", "", -1))
        print(data)
        break;
      # if (headers.end)
    except Exception as err:
      print(err)
      break
    # data = binary.split(carriage_return, 1)
  return header

def get_http(url):
  url_data = url_regex.findall(url)[0]
  scheme = url_data[1]
  host = url_data[2]
  path = url_data[3]
  file_name = url_data[5]

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((host, 80))

  command = (f'GET {path}{file_name} HTTP/1.0{carriage_return}').encode()

  sock.send(command)

  header = get_header(sock)
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
      currunt_block_size += block_size
    print(f'Download Complete: {file_name}, {file_size}/{file_size}')
  sock.close()

url = 'http://netapp.cs.kookmin.ac.kr/member/palladio.JPG'
get_http(url)
