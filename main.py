import requests

fileName = 'favicon.ico'
url = f'https://www.facebook.com/{fileName}'
r = requests.get(url, allow_redirects=True)
open(fileName, 'wb').write(r.content)

n1 = input()
n2 = input()
 
print(n1 + n2)