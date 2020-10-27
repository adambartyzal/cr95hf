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
  Rin = 330 * 2
  L0 = 470e-9 #vláďa vybral
  C0 = 220e-12 #vláďa vybral
  Rout = 27 #datasheet
  Zout = Rout
  w = 2 * m.pi * f

  C1 = 47e-12
  CS = C1 * 2
  CP = 147e-12

  Lant = 600e-9 #eDesign Antenna
  Rant = 0.24 #2 multimetry
  Zant = Rant + 1j * w * Lant
  Zant = 2.3 + 53 * 1j # změřeno VNA
  Qant = w * Lant / Rant


  ZC0 = 1 / (1j * w * C0)
  ZL0 = 1j * w * L0

  ZCS = 1 / (1j * w * CS)
  ZCP = 1 / (1j * w * CP)


  ZCin = 1 / (1j * w * Cin)
  Zin = ZCin + Rin

  Zload = ZL0 + par(ZC0,ZCS + par(Zin,Zant,ZCP))

  fc = 1/(2 * m.pi * m.sqrt(L0 * C0))

  return Zload
  #print(f'fc = {round((fc/1e6),2)} MHz, Zout = {Zout}, Zload = {cmath.polar(Zload)}')


freqs = range(10000000,20000000,1000)
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
plt.ylim(-m.pi,m.pi)
plt.grid()
plt.show()
