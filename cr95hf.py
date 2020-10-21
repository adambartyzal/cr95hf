import serial as s
import time as t

class Cr95hf:
  """Class for controling cr95hf over serial line"""

  def __init__(self):
    """Constructor of nfc object with default values"""
    self.ser = s.Serial('/dev/ttyUSB0', 57600,timeout=1)
    self.CL1 = ""
    self.CL2 = ""

  def wake(self):
    """sends wake puls and waits"""
    self.ser.write(b"\x55")
    self.ser.read(1)

  def echo(self):
    """sends echo end expects the same answer"""
    self.ser.write(b"\x55")
    if (self.ser.read(1) == b"\x55"):
      print('Echo OK')
    else:
      print('echo error')

  def info(self):
    """info about device"""
    self.ser.write(b"\x01\x00")
    print(f'IDN: {self.ser.read(17).hex()}')

  def protocol(self, type):
    """selects card type protocol"""
    if (type == 'A'):
      self.ser.write(b"\x02\x02\x02\x00")
    elif(type == 'B'):
      self.ser.write(b"\x02\x02\x03\x01")
    elif(type == 'N'):
      self.ser.write(b"\x02\x02\x00\x00")
    else:
      print('Wrong Protocol Selection')
    resp = self.ser.read(2)
    if (resp.hex() == "0000"):
      print(f'RF Type {type}')
    else:
      print('RF error')

  def reqA(self):
    """sends REQA and returns length of UID (-1 if none)"""
    self.ser.write(b"\x04\x02\x26\x07")
    resp = self.ser.read(7)
    if (resp.hex() == "8700"):
      print('No card')
    elif (resp.hex() == "80050400280000"):
      return 4
    elif (resp.hex() == "80054403280000" or resp.hex() == "80054400280000"):
      return 7
    else:
      return -1

  def request(self,type):
    """sends REQ(type) and returns length of UID (-1 if none)"""
    if (type == 'A'):
      self.ser.write(b"\x04\x02\x26\x07")
    elif(type == 'B'):
        self.ser.write(b"\x04\x03\x05\x00\x00")

    resp = self.ser.read(14)
    if (resp.hex() == "8700"):
      print('No card')
    elif (resp.hex() == "80050400280000"):
      return 4
    elif (resp.hex() == "80054403280000" or resp.hex() == "80054400280000"):
      return 7
    else:
      return -1

  def anticol1(self):
    """cascade level 1 anticolision"""
    self.ser.write(b"\x04\x03\x93\x20\x08")
    self.CL1 = self.ser.read(10).hex().upper()

  def anticol2(self):
    """cascade level 2 anticolision"""
    select1 = b'\x04\x08\x93\x70' + bytearray.fromhex(self.CL1[4:16])
    self.ser.write(select1)
    resp = self.ser.read(8)
    self.ser.write(b"\x04\x03\x95\x20\x08")
    self.CL2 = self.ser.read(10).hex().upper()

