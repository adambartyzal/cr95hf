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

  def readArcB(self):
    """Reads ARC_B register value."""
    self.ser.write(b"\x09\x03\x68\x00\x01")
    resp = self.ser.read(2)
    if (resp.hex() == "0000"):
      print(f'Gain set')
    else:
      print('Error')
    self.ser.write(b"\x09\x03\x68\x00\x01")
    resp = self.ser.read(2)
    print(resp.hex())

  def setArcB(self,index,gain):
    """
    Sets gain and modulation index.
      Parameters:
        index (char): 1 = 10%; 2 = 17%; 3 = 25%; 4 = 30%; 5 = 33%; 6 = 36%; D = 95% 
        gain (char): 0 = 34dB; 1 = 32dB; 3 =  27dB; 7 = 20dB; F = 8dB 
    """
    arc_b = bytearray.fromhex(gain + index)
    self.ser.write(b"\x09\x04\x68\x01\x01" + arc_b)
    resp = self.ser.read(2)
    if (resp.hex() == "0000"):
      print(f'Gain set')
    else:
      print('Gain setting error')

  def syncTime(self):
    """Set recomennded gain for type 2 and type 4 tags."""
    self.ser.write(b"\x09\x04\x3A\x00\x58\x04")
    resp = self.ser.read(2)
    if (resp.hex() == "0000"):
      print(f'Sync time optimized')
    else:
      print('Sync time optimization error')

  def request(self,type):
    """
    Sends REQ and returns length of UID (-1 if none).
      Parameter:
        type (char): 'A' = ISO/IEC 14443 Type A, 'B' = ISO/IEC 14443 Type B
    """
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
