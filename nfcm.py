import serial as s
import time as t
import sys

"""Script for testing CR95HF Protocol"""

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


  
  nfcm.write(b"\x01\x00") #info about the device
  resp = nfcm.read(17)
  print(f'IDN: {resp.hex()}')
  
  nfcm.write(b"\x02\x02\x02\x00") # choose:O/IEC 14443 Type A | No additional data
  resp = nfcm.read(2)

  if (resp.hex() == "0000"):
    print('RF Type A On')
  else:
    print('err')
    sys.exit()

  nfcm.write(b"\x04\x02\x26\x07") # send REQA
  resp = nfcm.read(7)

  if (resp.hex() == "8700"):
    print('No Type A card read')
    
  elif (resp.hex() == "80050400280000"):
    print(f'Cardtype: 4 byte UID')
    nfcm.write(b"\x04\x03\x93\x20\x08") # anticol 1
    resp = nfcm.read(10)
    CL1 = resp.hex().upper()
    UID = CL1[4:12]
    print(f'Serial Num: {UID}')
  
  elif (resp.hex() == "80054403280000" or resp.hex() == "80054400280000"):
    print(f'Cardtype: 7 byte UID')

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
  
  else:
    print(f'ATQA: {resp.hex()}')
    print(f'Other type of card!')

  nfcm.write(b"\x02\x02\x00\x00") #rf off
  resp = nfcm.read(2)
  if (resp.hex() == "0000"):
    print('RF Off')
  else:
    print('err')
    sys.exit()

###################################################################################################

  nfcm.write(b"\x02\x04\x03\x01\x20\x80") # choose:O/IEC 14443 Type B | Append crc
  resp = nfcm.read(2)

  if (resp.hex() == "0000"):
    print('RF Type B On')
  else:
    print('err')
    sys.exit()


#  nfcm.write(b"\x09\x04\x68\x01\x01\x30") # increase demodulation gain (from st forum)
#  resp = nfcm.read(20)
#
#  if (resp.hex() == "0000"):
#    print('Ok')
#  else:
#    print('err')
#    sys.exit()

  nfcm.write(b"\x04\x03\x05\x00\x00")
  resp = nfcm.read(20)

  if (resp.hex() == "8700"):
    print('No Type B card read')
  else:  
    print(f'ATQB: {resp.hex()}')

  nfcm.write(b"\x02\x02\x00\x00") #rf off
  resp = nfcm.read(2)
  if (resp.hex() == "0000"):
    print('RF Off')
  else:
    print('err')
    sys.exit()


###############################################################################

#nfcm.write(b"\x02\x02\x04\x51") # choose:O/IEC 14443 Type C
#resp = nfcm.read(2)
#if (resp.hex() == "0000"):
#  print('RF Type C On')
#else:
#  print('err')
#  sys.exit()

#nfcm.write(b"\x04\x05\x00\xFF\xFF\x00\x00") # send REQC
#  resp = nfcm.read(20)
#
#  if (resp.hex() == "8700"):
#    print('No Type C card read')
#  else:  
#    print(f'ATQC: {resp.hex()}')
#