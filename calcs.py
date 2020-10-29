import math as m
import numpy as np 
import matplotlib.pyplot as plt

def par(*args):
  s = 0
  for arg in args:
    s += 1 / arg
  return 1 / s

def compute(f):
  Cin = 22e-12 #datasheet
  Rin = 80e3 #datasheet
  Rout = 27 #datasheet
  L0 = 470e-9 #vláďa vybral
  C0 = 220e-12 #vláďa vybral
  
  Ratt = 330 #podle demo desky
  C1 = 70e-12
  C2 = 180e-12

  Zout = Rout
  w = 2 * m.pi * f

  Lant = 600e-9 #eDesign Antenna
  Rant = 0.24 #2 multimetry
  Zant = Rant + 1j * w * Lant
  #Zant = 2.3 + 53 * 1j # změřeno VNA

  ZC0 = 1 / (1j * w * C0 / 2)
  ZL0 = 1j * w * L0 * 2

  ZC1 = 1 / (1j * w * C1 * 2)
  ZC2 = 1 / (1j * w * C2)

  ZCin = 1 / (1j * w * Cin)
  Zin = par(ZCin,Rin) + Ratt * 2

  Zload = ZL0 + par(ZC0,ZC1 + par(Zin,Zant,ZC2))

  fc = 1/(2 * m.pi * m.sqrt(L0 * C0))

  return Zload
  #pRattt(f'fc = {round((fc/1e6),2)} MHz, Zout = {Zout}, Zload = {cmath.polar(Zload)}')


freqs = range(int(10e6),int(20e6),int(1e4))
Zmags = []
Zangs = []
for x in freqs:
  z = compute(x)
  Zmags.append(abs(z))
  Zangs.append(np.angle(z))

fig, ax_left = plt.subplots()
ax_right = ax_left.twinx()

ax_left.plot(freqs, Zmags, color='black')
ax_right.plot(freqs, Zangs, color='red')
plt.ylim(-m.pi/2,m.pi/2)
plt.grid()
plt.show()
