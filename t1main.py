import numpy as np
import matplotlib.pyplot as plt
from CoolProp.CoolProp import PropsSI
color= 'pink'
Th = 35 + 273 #[K]
qL = 1000 #[W] 1 J/s - 1 W
Tl = 5 + 273 #[K] valor intermediario do armazenamento das Vacinas Pfizer
#compressor isentropico
fluid = 'R134a'
h1 = PropsSI("H", "T", Tl, "Q", 1, fluid)
s1 = PropsSI("S", "T", Tl, "Q", 1, fluid)
s2=s1
P3 = PropsSI("P", "T", Th, "Q", 0, fluid)
P2 = P3 
T2 = PropsSI("T", "S", s2, "P", P2, fluid)
h2 = PropsSI("H", "T", T2, "S", s2, fluid)
h3 = PropsSI("H", "P", P3, "Q", 0, fluid)
h4=h3  
m_dot = qL / (h1 - h4)
qH = m_dot *(h2-h3)
wEnt = m_dot * (h2-h1) #[W]
COP = qL / wEnt 
P1= PropsSI("P", "T", Tl, "Q", 1, fluid)
P4 = P1
print('mponto=  %.4f' %(m_dot))
print('qH=  %.2f' %(qH))
print('wEnt=  %.2f' %(wEnt))
print('COP=  %.2f' %(COP))


# Generate some diagrams
# Let figure 1 be a P-h diagram
plt.rc('font', size=14) 
# This is a True/False flag to deactivate the plot text
show_text = True
# This is a True/False flag to allow over-plotting of previous results
clear_plots = True

f1 = plt.figure(1,)
if clear_plots:
    plt.clf()
ax1 = f1.add_subplot(111)
ax1.set_xlabel('Enthalpy, h (kJ/kg)')
ax1.set_ylabel('Pressure, P (bar)')
ax1.set_title('Vapor compression Cycle P-h Diagram')


# Generate the dome on both plots

Tt = PropsSI("TTRIPLE",fluid)
Pt = PropsSI("PTRIPLE",fluid)

Tc = PropsSI("TCRIT",fluid)
Pc = PropsSI("PCRIT",fluid)

T = np.arange(Tt,Tc,2.5)

hL = 1e-3*np.array([
  PropsSI("H","T",Ti,"Q",0,fluid) for Ti in T
])
hV = 1e-3*np.array([
  PropsSI("H","T",Ti,"Q",1,fluid) for Ti in T
])
P = 1e-5*np.array([
  PropsSI("P","T",Ti,"Q",0,fluid) for Ti in T
])

ax1.plot(hL,P,'k')
ax1.plot(hV,P,'k')
#Plota a a curva do fluido

# Process 1-2
p = np.linspace(P1,P2)
h = np.array([PropsSI("H","P",Pi,"S",s1,fluid) for Pi in p])
ax1.plot(h*1e-3,1e-5*p,color,linewidth=1.5)

# Process 2-3
ax1.plot(1e-3*np.array([h2,h3]),1e-5*np.array([P2,P3]),color,linewidth=1.5)

# Process 3-4
ax1.plot(1e-3*np.array([h3,h4]),1e-5*np.array([P3,P4]),color,linewidth=1.5)

# Process 4-5
ax1.plot(1e-3*np.array([h4,h1]),1e-5*np.array([P4,P1]),color,linewidth=1.5)

ax1.grid('on')
ax1.set_yscale('log')

ax1.set_ylim(bottom = 1)
ax1.set_xlim(left = 100)

plt.show()
