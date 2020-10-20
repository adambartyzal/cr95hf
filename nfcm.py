import serial as s
#import time as t
import sys

with s.Serial('/dev/ttyUSB0', 57600, timeout=1) as nfcm:

  nfcm.write(b"\x55") #wake puls t1
  resp = nfcm.read(1)

  nfcm.write(b"\x55") #send echo
  resp = nfcm.read(1)
  
  if (resp.hex() == "55"):
    print('Echo OK')
  else:
    print('err')
    sys.exit()
 
  nfcm.write(b"\x02\x02\x02\x00") # choose:O/IEC 14443 Type A
  resp = nfcm.read(2)

  if (resp.hex() == "0000"):
    print('RF On')
  else:
    print('err')
    sys.exit()

  nfcm.write(b"\x04\x02\x26\x07") # send ATQ
  resp = nfcm.read(7)
  print(f'ATQ: {resp.hex()}')

  if (resp.hex() == "80050400280000"):
    print(f'Cardtype: Classic 1k')
    nfcm.write(b"\x04\x03\x93\x20\x08") # anticol 1
    resp = nfcm.read(10)
    CL1 = resp.hex().upper()
    UID = CL1[4:12]
    print(f'Serial Num: {UID}')
  
  elif (resp.hex() == "80054403280000"):
    print(f'Cardtype: DESFIRE')

    nfcm.write(b"\x04\x03\x93\x20\x08") # anticol 1
    resp = nfcm.read(10)
    CL1 = resp.hex().upper()

    select1 = b'\x04\x08\x93\x70' + bytearray.fromhex(CL1[4:16]) # prepare sendRecv select1
    nfcm.write(select1)
    resp = nfcm.read(8)
    select1resp = resp.hex().upper()

    nfcm.write(b"\x04\x03\x95\x20\x08") # anticol 2
    resp = nfcm.read(10)
    CL2 = resp.hex().upper()

    UID = CL1[6:12] + CL2[4:12]
    print(f'Serial Num: {UID}')

  elif (resp.hex() == "8700"):
    print('No card read')

  else:
    print(f'Other type of card!')

    nfcm.write(b"\x04\x03\x95\x20\x08")
    resp = nfcm.read(10)
    print(f'CL2 is {resp.hex()}')
    #print(f'Serial Num: {}')


  nfcm.write(b"\x02\x02\x00\x00") #rf off
  resp = nfcm.read(2)
  if (resp.hex() == "0000"):
    print('RF Off')
  else:
    print('err')
    sys.exit()
