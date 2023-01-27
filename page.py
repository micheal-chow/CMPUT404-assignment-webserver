#!/usr/bin/env python3
from datetime import datetime, timezone

class Page:
    def get_date(self):
        return datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    def set_code(self, code):
        self.code = code
        
    def set_url(self, base_url, real_url):
        self.base_url = base_url
        self.real_url = real_url
        
    def set_content_type(self, type):
        self.contentType = type
        
    def set_filepath(self, filepath):
        self.filepath = filepath
        
    def set_message_description(self):
        if self.code == 200:
            self.message = "OK"
            self.description = "Everything is OK."
        
        elif self.code == 301:
            self.message = "Moved Permanently"
            self.description = "The requested resource has been moved permanently."
        
        elif self.code == 404:
            self.message = "Not Found"
            self.description ="The requested resource was not found."
        
        elif self.code == 405:
            self.message = "Method Not Allowed"
            self.description = "Method not allowed."
            
        else:
            self.message = "Unknown"
            self.description = "An unknown error has occur"

    def make_header(self):
        self.header = f"""HTTP/1.1 {self.code} {self.message}\r
Server: A1 Server\r
Content-Type:{self.contentType}\r
Content-Length:{self.contentLength}\r
Date: {self.get_date()}\r\n
        """
        if self.code == 301:
            self.header += f"Location: {self.real_url}\r\n"
            
    def make_body(self):
        if self.code == 200:
            with open(self.filepath, encoding="utf-8") as f:
                self.content = f.read()
                return
            
        else:
            content = f"""<!DOCTYPE html>
<html>
<head>
<title>{self.code} {self.message}</title>
</head>
<body>
<h1>{self.code} {self.message}</h1>
{self.description}\n
            """
            if self.code == 301:
                content += f"\nYou can find the new resource <a href=\"{self.real_url}\">here.</a>\n"
            content += "</body>\n</html>"
            
            self.content = content
            
    def build_page(self):
        self.set_message_description()
        self.make_body()
        self.contentLength = self.content.encode("utf-8")
        self.make_header()
        page = self.header + self.content
        return page
        
            
    
            
    