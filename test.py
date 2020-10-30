from cr95hf import Cr95hf

UID = ''

nfc = Cr95hf()
nfc.wake()
nfc.echo()
nfc.info()
nfc.protocol('A')
nfc.readArcB()
nfc.setArcB('D','7')
nfc.readArcB()
#nfc.syncTime()
uidLength = nfc.request('A')

if (uidLength == 4):
  nfc.anticol1()
  UID = nfc.CL1[4:12]
elif(uidLength == 7):
  nfc.anticol1()
  nfc.anticol2()
  UID = nfc.CL1[6:12] + nfc.CL2[4:12]
if (len(UID) != 0):
  print(f'Serial Num: {UID}')
nfc.protocol('N')

nfc.protocol('B')
nfc.readArcB()
nfc.setArcB('2','7')
nfc.readArcB()
#nfc.syncTime()
nfc.wakeupB()
nfc.request('B')
nfc.protocol('N')
del nfc
