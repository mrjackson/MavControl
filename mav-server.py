#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import time
import serial #python3 -m pip install pyserial
import argparse
import json

hostName = "192.168.10.25"
hostPort = 9000

def mavsend(command):
   ser = serial.Serial('/dev/ttyUSB0', 9600)
   ser.write(command.encode())
   mavrecv = ser.readline()
   ser.close()
   return mavrecv.decode()

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # curl http://192.168.10.25:9000/api/av
        self.send_header("Content-type", "application/json")
        data = ""
        ttype = ""
        if self.path == "/api/av":
            ttype = "!"
        elif self.path == "/api/a":
            ttype = "$"
        elif self.path == "/api/v":
            ttype = "%"

        for i in range(1,17,1):
            results = (mavsend("v" + str(i) + ttype))
            results = "\"Out" + "{0:02d}".format(i) + "\": \"" + results[8:10] + "\""
            if i < 16:
                data = data + results + ", "
            else:
                data = data + results
        self.wfile.write(bytes("{" + data + "}", "utf-8"))
        print("----- SOMETHING WAS GET!! ------")

#        self.send_response(200)
#        self.send_header("Content-type", "application/json")
#        self.end_headers()
#        self.wfile.write(bytes("<html><head><title>Title goes here.</title></head>", "utf-8"))
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        # self.wfile.write("<p>You accessed path: %self</p>" % self.path)
#        self.wfile.write(mavsend("v01$").encode('utf-8'))

    def do_POST(self):
        # curl -X POST -d '{"Output": "04", "Input": "01"}' http://192.168.10.25:9000/api/av
        print("post")
        length = int(self.headers['Content-Length'])
        content = self.rfile.read(length)
        parsed_json = json.loads(content.decode("utf8"))
        ttype = ""
        print(self.path)
        if self.path == "/api/av":
            ttype = "!"
        elif self.path == "/api/a":
            ttype = "$"
        elif self.path == "/api/v":
            ttype = "%"

        output = parsed_json['Output']
        input = parsed_json['Input']
        mavrecev = mavsend(str(input) + "*" + str(output) + ttype)
        self.wfile.write(mavrecev.encode('utf-8'))

        print("----- SOMETHING WAS POST!! ------")
#        print(self.headers)
#        print(content.decode())

#        self.wfile.write(self.path.encode('utf-8'))
#        print("test post")
#        print(self.path)
myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))


#curl -X POST -d '{"on":true,"ct":500,"bri":0}' http://192.168.10.25:9000/api/MrJacksonHue/lights/3/state
