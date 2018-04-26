#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import time
import serial
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
        print("GET")

    def do_POST(self):
        # curl -X POST -d '{"Output": "04", "Input": "01"}' http://192.168.10.25:9000/api/av
        print("post")


    def do_PUT(self):
        # curl -X PUT -d '{"Output": "04", "Input": "01"}' http://192.168.10.25:9000/api/av
        print("put")

myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))


#curl -X POST -d '{"on":true,"ct":500,"bri":0}' http://192.168.10.25:9000/api/MrJacksonHue/lights/3/state
