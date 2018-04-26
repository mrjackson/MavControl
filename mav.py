#!/usr/bin/env python3

import serial
import argparse

def mavsend(command):
   ser = serial.Serial('/dev/ttyUSB0', 9600)
   ser.write(command.encode())
   mavrecv = ser.readline()
   ser.close()
   return mavrecv.decode()

parser = argparse.ArgumentParser()
parser.add_argument('--tieav', '-tav',nargs=2,type=int,help='Tie' )
parser.add_argument('--tieaudio', '-ta',nargs=2,help='Tie Audio' )
parser.add_argument('--tievideo', '-tv',nargs=2,help='Tie Video' )
parser.add_argument('--viewav', '-vav',nargs=1,type=int,help='View' )
parser.add_argument('--viewaudio', '-va',nargs=1,help='View Audio' )
parser.add_argument('--viewvideo', '-vv',nargs=1,help='View Video' )
parser.add_argument('--preset', '-p',nargs=1,help='Tie Presets' )
parser.add_argument('--raw', '-r',nargs=1,help='Send RAW command' )
parser.add_argument('--curaudio', '-ca',action='store_true',help='Current Audio Ties' )
parser.add_argument('--curvideo', '-cv',action='store_true',help='Current Video Ties' )

args = parser.parse_args()
 
if args.tieav:
   mavsend(str(args.tieav[0]) + "*" + str(args.tieav[1]) + "!")
elif args.tieaudio:
   mavsend(str(args.tieaudio[0]) + "*" + str(args.tieaudio[1]) + "$")
elif args.tievideo:
   mavsend(str(args.tievideo[0]) + "*" + str(args.tievideo[1]) + "&")
elif args.viewav:
   print(mavsend("v" + str(args.viewav[0]) + "!"))
elif args.viewaudio:
   print(mavsend("v" + str(args.viewaudio[0]) + "$"))
elif args.viewvideo:
   print(mavsend("v" + str(args.viewvideo[0]) + "&"))
elif args.raw:
  print(mavsend(str(args.raw)))
elif args.preset:
   if str(args.preset[0]) == "1": # BT to All
      print("BT Preset")
      mavsend("1*1$")
      mavsend("1*2$")
      mavsend("1*3$")
      mavsend("1*14$")
      mavsend("1*16$")
   elif str(args.preset[0]) == "2": # TV to All
      print("Reciever Preset")
      mavsend("2*1$")
      mavsend("2*2$")
      mavsend("2*3$")
      mavsend("2*14$")
      mavsend("2*16$")
   elif str(args.preset[0]) == "3": # TV to All
      print("TV Preset")
      mavsend("3*1$")
      mavsend("3*2$")
      mavsend("3*3$")
      mavsend("3*14$")
      mavsend("3*16$")
elif args.curaudio:
   data = ""
   for i in range(1,17,1):
      results = (mavsend("v" + str(i) + "$"))
      results = "\"Out" + "{0:02d}".format(i) + "\": \"" + results[8:10] + "\""
      if i < 16:
         data = data + results + ", "
      else:
         data = data + results
#      print(results)
   print("{" + data + "}")
elif args.curvideo:
   for i in range(1,17,1):
      results = (mavsend("v" + str(i) + "&"))
      results = results[8:10] + ":" + "{0:02d}".format(i)
      print(results)
else:
   print("~ No Flag")

#ser = serial.Serial('/dev/ttyUSB0', 9600)
#ser.write(b'16!')
#print(ser.readline())
#ser.close()             # close port



