import json

import requests
import urllib.parse as urlparsethis
# !coding=UTF-8
from http.server import HTTPServer, BaseHTTPRequestHandler
import io, shutil, urllib
# import speech_recognition as sr
# r=sr.Recognizer()
# print(sr.__version__)
# hardPseech=sr.AudioFile('harvard.wav')
# with hardPseech as source:
#     audio=r.record(source)
# textcont=r.recognize_google(audio,language='zh-CN')
# print(textcont)

import speech_recognition as sr
#
# r = sr.Recognizer()
#
# test = sr.AudioFile('harvard.wav')
#///VwR3Et7-I1fwbheijY-e8Vl9Bxuip6RoEgav-Gq-nqC2   https://stream.watsonplatform.net/speech-to-text/api
# harvard = sr.AudioFile('harvard.wav')
# r = sr.Recognizer()
# with harvard as source:
#     audio = r.record(source)
# print(type(audio))
#
# IBM_USERNAME = '************************'
# IBM_PASSWORD = '************************'
#
# text = r.recognize_google(audio, username=IBM_USERNAME, password=IBM_PASSWORD, language='zh-CN')
# print(text)



class MyHttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        name = "World"
        selfqueryString=''
        callback = ''
        if '?' in self.path:  # 如果带有参数
            selfqueryString = urllib.parse.unquote(self.path.split("para=", 1)[1])
            callback = urllib.parse.unquote(self.path.split("callback=", 1)[1])
            callback=callback.split("&")[0]

        # name=str(bytes(params['name'][0],'GBK'),'utf-8')
        # params = urllib.parse.parse_qs(self.queryString)
        url=selfqueryString
        jsLoads = json.loads(url)

        urlupload=jsLoads["c"]
        wavpath = jsLoads["d"]
        varResponse=self.sendFile(urlupload, wavpath)
        print(urlupload)
        print(wavpath)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write((callback+'({"result":'+varResponse+'})').encode())
        print("do_GET")

        # parsed = urlparse.urlparse(self.queryString)
        # querys = urlparse.parse_qs(parsed.query)
        # print(querys)

        # query = urlparse.urlparse(url).query
        # dddddict= dict([(k, v[0]) for k, v in urlparse.parse_qs(query).items()])
        # print(jsLoads)
        # print(jsLoads)

        # vardata = parse_url(self.queryString);
        # print(params)
        # urlc=params.para["c"]
        # processid = params["ProcessID"][0]
        # testwav = params["ProcessID"][""]
        #
        # params.para.c
        # name = params["name"][0] if "name" in params else None
        # sendFile(argurl, argfilepath)
        # r_str = "Hello " + name + " <form action='' method='POSt'>Name:<input name='name' /><br /><input type='submit' value='submit' /></form>"
        # enc = "UTF-8"
        # encoded = ''.join(r_str).encode(enc)
        # f = io.BytesIO()
        # f.write(encoded)
        # f.seek(0)
        # self.send_response(200)
        # self.send_header("Content-type", "text/html; charset=%s" % enc)
        # self.send_header("Content-Length", str(len(encoded)))
        # self.end_headers()
        # shutil.copyfileobj(f, self.wfile)

    def do_POST(self):
        s = str(self.rfile.readline(), 'UTF-8')  # 先解码
        print(urllib.parse.parse_qs(urllib.parse.unquote(s)))  # 解释参数
        self.send_response(301)  # URL跳转
        self.send_header("Location", "/?" + s)
        self.end_headers()

    def sendFile(ddself,argurl, argfilepath):
        # url = 'http://10.0.0.21:9001/api/Core/UploadFile?ProcessID=11111&TenantID=9'
        # url = 'https://lvyan.test.lv-yan.com/api/Core/UploadFile?ProcessID=111111111111&TenantID=9'

        # url = 'http://www.test.com/doPost.php'
        # files = {'file': open('D:/tmp/1.jpg', 'rb')}

        # 要上传的文件
        files = {'file123': ('test.wav', open(argfilepath, 'rb'))
                 }  # 显式的设置文件名

        # post携带的数据
        data = {'a4324': 'oliver zhang', 'b23452345': 'https 上传文件'}

        r = requests.post(argurl, files=files, data=data)
        print(r.text)
        return r.text



if __name__ == '__main__':
    # server = HTTPServer(host, Resquest)
    # print("Starting Server....")
    # server.serve_forever()
    httpd = HTTPServer(('', 13001), MyHttpHandler)
    print("Server started on 127.0.0.1,port 13001.....")
    httpd.serve_forever()


#
# if __name__ == '__main__':
#     app.run()

def sendFile(argurl, argfilepath):
    # url = 'http://10.0.0.21:9001/api/Core/UploadFile?ProcessID=11111&TenantID=9'
    # url = 'https://lvyan.test.lv-yan.com/api/Core/UploadFile?ProcessID=111111111111&TenantID=9'

    # url = 'http://www.test.com/doPost.php'
    # files = {'file': open('D:/tmp/1.jpg', 'rb')}

    # 要上传的文件
    files = {'file123': ('test.wav', open(argfilepath, 'rb'))
             }  # 显式的设置文件名

    # post携带的数据
    data = {'a4324': 'oliver zhang', 'b23452345': 'https 上传文件'}

    r = requests.post(argurl, files=files, data=data)
    print(r.text)
