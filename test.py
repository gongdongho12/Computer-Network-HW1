import socket
import re

carriage_return = '\r\n\r\n'
single_byte = 1
header_regex = re.compile("(.*)\: (.*)")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('netapp.cs.kookmin.ac.kr', 80))

command = (f'GET http://netapp.cs.kookmin.ac.kr/member/palladio.JPG HTTP/1.0{carriage_return}').encode()

sock.send(command)

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
          headers = re.findall(r'(.*)\: (.*)', data)
          for header_data in headers:
            print(f'{header_data[0]} : {header_data[1]}')
            header[header_data[0]] = (header_data[1].replace("\r", "", -1))
          # while True:
          #   if (m == None):
          #     break
          #   print(m.group())
          print(data)
          break;
        # if (headers.end)
      except Exception as err:
        print(err)
        break
    # data = binary.split(carriage_return, 1)

get_header(sock)
sock.close()
