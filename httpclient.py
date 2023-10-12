#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        code_data = data.split(" ")
        #print(code_data)
        code_data = code_data[1]
        code_data = int(code_data)
        return code_data

    def get_headers(self,data):
        the_header = data.split("\r\n\r\n")[0]
        #print(the_header)
        return the_header

    def get_body(self, data):
        
        body_data = data.split("\r\n\r\n")
        #print("body_data ->", body_data)
        
        if body_data is None or (body_data[1]=="[]"):
            HTML_data= ''
        else:    
            HTML_data = body_data[1]
        #print("body_data at 1", HTML_data)#eg 
        
        
        
        return HTML_data
        
        return None
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        code = 500
        body = ""
    
        #print("the url->,"url)

        
        parsed_url = urllib.parse.urlparse(url)#ParseResult(scheme='http', netloc='127.0.0.1:27663', path='/49872398432', params='', query='', fragment='')
        #print("the url post parse->", parsed_url)
        derived_scheme = parsed_url.scheme#http
        derived_host = parsed_url.hostname#127.0.0.1
        derived_port = parsed_url.port#27663
        derived_query = parsed_url.query#''
        
        #print("\nthe url for GET->", url)
        #print("the parsed_url->", parsed_url)
        #print("the scheme->",  derived_scheme)
        #print("the host->",  derived_host)
        #print("the port->",  derived_port)
        #print("the query->",  derived_query + "\n")



        if (derived_port == None) and (derived_scheme == "http"):# so if we arn't given a port, then set the port to the following
            derived_port = 80#see https://developer.mozilla.org/en-US/docs/Glossary/Port for why its 80
        
        if (derived_port == None) and (derived_scheme == "https"):
            derived_port = 443  #see https://developer.mozilla.org/en-US/docs/Glossary/Port for why its 443
                
        
        self.connect(derived_host, derived_port)#make the connection
        
        get_request = f'GET {url} HTTP/1.1\r\nHost: {derived_host}\r\nConnection: Closed\r\n\r\n'
        
        self.sendall(get_request)#make the request
        
        data_returned = self.recvall(self.socket)#get the data we are given back
        #print("data returned->", data_returned)
        
        body = self.get_body(data_returned) #returns the HTML data
        code = self.get_code(data_returned) #returns the code. i.e 200 or 404 or 301 etc...
        #print("the body->\n", body)
        #print("the code->", code)

        
        
        self.close()
        
        return HTTPResponse(code, body)#make the return










    def POST(self, url, args=None):
        code = 500
        body = ""
        
        #print("the url->,"url)
        
        parsed_url = urllib.parse.urlparse(url)
        #print("the url post parse->", parsed_url)
        derived_scheme = parsed_url.scheme
        derived_host = parsed_url.hostname
        derived_port = parsed_url.port
        derived_query = parsed_url.query
        
        #print("\nthe url for POST->", url)
        #print("the parsed_url->", parsed_url)
        #print("the scheme->",  derived_scheme)
        #print("the host->",  derived_host)
        #print("the port->",  derived_port)
        #print("the query->",  derived_query + "\n")
  
  
        if (derived_port == None) and (derived_scheme == "http"):
            derived_port = 80#see https://developer.mozilla.org/en-US/docs/Glossary/Port for why its 80
        
        if (derived_port == None) and (derived_scheme == "https"):
            derived_port = 443#see https://developer.mozilla.org/en-US/docs/Glossary/Port for why its 443   
        
                
        if args == None:
            args = " "
        else:
            print("THE ARGS NOT EMPTY-> " , args)
            args = urllib.parse.urlencode(args)
            print("\nTHE ARGS->" , args , "\n")
            
            
        length_of_args = len(args)
            
        post_request = f"POST {url} HTTP/1.1\r\nHost: {derived_host}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {length_of_args}\r\nConnection: close\r\n\r\n{args}"

        self.connect(derived_host, derived_port)
        self.sendall(post_request)
        
        data_returned = self.recvall(self.socket)
        
        body = self.get_body(data_returned)
        code = self.get_code(data_returned)
        
        self.close()
        
        
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
