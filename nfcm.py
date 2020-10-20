import serial as s
#import time as t
import sys

with s.Serial('/dev/ttyUSB0', 57600, timeout=2) as nfcm:
  
  nfcm.write(b"\x55") #wake puls t1
  resp = nfcm.read(1)
  #print(f'Response is {resp.hex()}')

  nfcm.write(b"\x55") #send echo
  resp = nfcm.read(1)
  #print(f'Response is {resp.hex()}')
  
  if (resp.hex() == "55"):
    print('Echo OK')
  else:
    print('err')
    sys.exit()
 
  nfcm.write(b"\x02\x02\x02\x00") # choose ISO/IEC 14443 Type A
  resp = nfcm.read(2)
  #print(f'Response is {resp.hex()}')

  if (resp.hex() == "0000"):
    print('RF On')
  else:
    print('err')
    sys.exit()
  
  nfcm.write(b"\x04\x02\x26\x07") # send ATQ
  resp = nfcm.read(7)
  print(f'ATQ: {resp.hex()}')

  nfcm.write(b"\x04\x03\x93\x20\x08")
  resp = nfcm.read(10)
  print(f'Serial Num: {resp.hex()[4:12].upper()}')
  
  nfcm.write(b"\x02\x02\x00\x00") #rf off
  resp = nfcm.read(2)
  #print(f'Response is {resp.hex()}')

  if (resp.hex() == "0000"):
    print('RF Off')
  else:
    print('err')
    sys.exit()
