import ssl
import urllib.request

client_id = ""
client_secret = ""

query = '아쿠아맨'
encText = urllib.parse.quote(query)
url = "https://openapi.naver.com/v1/search/blog?query=" + encText
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
response = urllib.request.urlopen(request, context=gcontext)
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)