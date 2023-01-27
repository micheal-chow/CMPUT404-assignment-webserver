#  coding: utf-8 
import socketserver
from os import path
from page import Page

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def get_absolute_path(self):
        return path.join(path.dirname(__file__),"www")
    
    def get_method(self):
        self.method = self.data.split()[0].decode("utf-8")
        
    def get_url(self):
        self.base_url = self.data.split()[1].decode("utf-8")
        self.url = self.base_url
        self.path_ending = True
        
        remove_traversal = self.url.split("../")
        remove_traversal = [path for path in remove_traversal if path]
        self.url = ''.join(remove_traversal)
        
        if not (self.base_url.endswith(".html") or self.base_url.endswith(".css") or self.base_url.endswith("/")):
            self.path_ending = False
            self.url += "/"
        
        if self.url.endswith("/"):
            self.url += "index.html"
        
    def get_filepath(self):
        self.filepath = self.get_absolute_path() + self.url

    
    def get_content_type(self):
        if self.url.endswith(".html"):
            self.type = "text/html"
        elif self.url.endswith(".css"):
            self.type = "text/css"
        else:
            self.type = "application/octet-stream"
            
    def get_code(self):
        if self.method != "GET":
            self.code = 405
            return
        
        if self.url_exists():
            if not self.path_ending:
                self.code = 301
            else:
                self.code = 200
            return
        else:
            self.code = 404
        
    def url_exists(self):
        self.get_filepath()
        try:
            file = open(self.filepath, "r")
            file.close()
        except:
            return False
        
        return True
        
        
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print ("Got a request of: %s\n" % self.data)
        
        page = Page()
        self.get_absolute_path()
        self.get_method()
        self.get_url()
        
        self.filepath = None
        self.get_code()
        self.get_content_type()
        
        # print(self.base_url, self.url, self.code, self.type, self.filepath, sep="\n",end="\n\n")
        
        page.set_code(self.code)
        if self.filepath:
            page.set_filepath(self.filepath)
        page.set_url(self.base_url, self.url)
        page.set_content_type(self.type)
        response = page.build_page()
        
        
        
        # self.request.sendall(bytearray("OK",'utf-8'))
        self.request.sendall(bytearray(response,'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
