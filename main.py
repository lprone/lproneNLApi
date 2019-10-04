import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from urllib.parse import parse_qs

import requests

HOST_NAME = 'localhost'
PORT_NUMBER = 80


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            response = "index"
            self.wfile.write(bytes("%s" % response, "utf8"))
            return
        elif '/question' in str(self.path):

            query_params = urlparse(self.path).query
            keyValue = parse_qs(query_params).get("key")

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # api-endpoint
            URL = "https://lpronechatbotapi.herokuapp.com/answer"
            PARAMS = {'key': keyValue}
            # sending get request and saving the response as response object
            r = requests.get(url=URL, params=PARAMS)

            response = r.text

            self.wfile.write(bytes(response, "utf8"))
            return
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            response = "File Not Found"
            self.wfile.write(bytes(response, "utf8"))
            return
        return


if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class(('', PORT_NUMBER), MyHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
