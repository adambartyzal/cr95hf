import serial as s

class Cr95hf:
  """Class for controling cr95hf over serial line."""

  def __init__(self):
    """Constructor of nfc object with default values."""
    self.ser = s.Serial('/dev/ttyUSB0', 57600,timeout=1)
    self.CL1 = ""
    self.CL2 = ""

  def __del__(self):
    self.ser.close()

  def wake(self):
    """Sends wake puls and waits."""
    self.ser.write(b"\x55")
    self.ser.read(1)

  def echo(self):
    """Sends echo end expects the same answer."""
    self.ser.write(b"\x55")
    if (self.ser.read(1) == b"\x55"):
      print('Echo OK')
    else:
      print('echo error')

  def info(self):
    """Info about device."""
    self.ser.write(b"\x01\x00")
    print(f'IDN: {self.ser.read(17).hex()}')

  def protocol(self, type):
    """
    Selects card type protocol.
      Parameter:
        type (char): 'A' = Type A, 'B' = Type B, 'N' = RF off)
    """
    if (type == 'A'):
      self.ser.write(b"\x02\x02\x02\x00")
    elif(type == 'B'):
      self.ser.write(b"\x02\x09\x03\x01\x00\x00\x00\xFF\x03\x00\xC8")
    elif(type == 'N'):
      self.ser.write(b"\x02\x02\x00\x00")
    else:
      print('Wrong Protocol Selection')
    resp = self.ser.read(2)
    if (resp.hex() == "0000"):
      print(f'RF Type {type}')
    else:
      print('RF error')

  def readArcB(self):
    """Reads ARC_B register value."""
    self.ser.write(b"\x09\x03\x68\x00\x01")
    resp = self.ser.read(2)
    if (resp.hex() != "0000"):
      print('ARC_B read error')
    self.ser.write(b"\x08\x03\x69\x01\x00")
    resp = self.ser.read(3)
    print(f'Current settings: {resp.hex()[4:6].upper()}')

  def setArcB(self,index,gain):
    """
    Sets gain and modulation index.
      Parameters:
        index (char): 1 = 10%; 2 = 17%; 3 = 25%; 4 = 30%; 5 = 33%; 6 = 36%; D = 95% 
        gain (char): 0 = 34dB; 1 = 32dB; 3 =  27dB; 7 = 20dB; F = 8dB 
      Defaults:
        Type A: 'DF'
        Type B: '2F'
      Recommended for demoboard:
        Type A: 'D3'
        Type B: '20'
    """
    arc_b = b"\x09\x04\x68\x01\x01" + bytearray.fromhex(index + gain)
    self.ser.write(arc_b)
    resp = self.ser.read(2)
    if (resp.hex() == "0000"):
      print(f'Option {index + gain} set')
    else:
      print('Gain setting error')

  def apgen(self):
    """Sends APGEN message sniffed from elatec reader."""
    self.ser.write(b"\x04\x04\x00\x0B\x3F\x80")
    print(self.ser.read(10).hex())

  def request(self,type):
    """
    Sends REQ and returns length of UID (-1 if none).
      Parameter:
        type (char): 'A' = ISO/IEC 14443 Type A, 'B' = ISO/IEC 14443 Type B
    """
    if (type == 'A'):
      self.ser.write(b"\x04\x02\x26\x07")
    elif(type == 'B'):
      self.ser.write(b"\x04\x03\x05\x00\x00") # AntiCol Prefix 05, AFI = \x00 means All Families respond, PARAM = \x00 means N = 1 therefore no waiting for slotmarker
    resp = self.ser.read(14)
    if (resp.hex() == "8700"):
      print('No card')
    elif (resp.hex() == "80050400280000"):
      return 4
    elif (resp.hex() == "80054403280000" or resp.hex() == "80054400280000"):
      return 7
    else:
      return -1

  def wakeupB(self):
    """Sends WUPB (same as REQB with wakeup bit up)."""
    self.ser.write(b"\x04\x03\x05\x00\x08")
    resp = self.ser.read(2)
    print(resp.hex())

  def anticol1(self):
    """Cascade level 1 anticolision."""
    self.ser.write(b"\x04\x03\x93\x20\x08")
    self.CL1 = self.ser.read(10).hex().upper()

  def anticol2(self):
    """Cascade level 2 anticolision."""
    select1 = b'\x04\x08\x93\x70' + bytearray.fromhex(self.CL1[4:16])
    self.ser.write(select1)
    resp = self.ser.read(8)
    self.ser.write(b"\x04\x03\x95\x20\x08")
    self.CL2 = self.ser.read(10).hex().upper()
