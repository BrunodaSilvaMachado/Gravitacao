#_*_ coding: utf-8 _*_
#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib import animation

GM = 4*np.pi**2
dt = 0.008

class Planeta():
	def __init__(self,nome,massa,x,y,vx,vy):
		self.n = nome
		self.m = massa
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy
		self.e = 0.5*massa*(x**2+y**2) - (GM*self.m)/self.ratio(x,y)
	def ratio(self,x,y):
		return np.sqrt(x**2+y**2)
		
	def move(self,x_e2,y_e2,vx_e2,vy_e2,m_2,m_s):
		r1 = self.ratio(self.x,self.y)
		r2 = self.ratio(x_e2,y_e2)
		r12= self.ratio((self.x-x_e2),(self.y-y_e2))
	
		self.x = self.x + self.vx*dt -4*np.pi**2*(m_2/m_s)*(self.x-x_e2)*(dt**2/r12**3)
		self.y = self.y + self.vy*dt -4*np.pi**2*(m_2/m_s)*(self.y-y_e2)*(dt**2/r12**3)
	
		self.vx +=  - 4*np.pi**2*(self.x*dt/r1**3) -4*np.pi**2*(m_2/m_s)*(self.x-x_e2)*(dt/r12**3)
		self.vy +=  - 4*np.pi**2*(self.y*dt/r1**3) -4*np.pi**2*(m_2/m_s)*(self.y-y_e2)*(dt/r12**3)
		
		self.e = 0.5*self.m*(self.x**2+self.y**2) - (GM*self.m)/self.ratio(self.x,self.y)
		
#end

def grafico(title,visivel):
	axes = plt.gca()
	axes.axes.get_xaxis().set_visible(visivel)
	axes.spines['top'].set_color('none')
	axes.spines['right'].set_color('none')
	axes.yaxis.set_ticks_position('left')
	axes.xaxis.set_ticks_position('bottom')
	axes.spines['bottom'].set_position(('data',0))
	axes.spines['left'].set_position(('data',0))
	plt.grid(True)
	plt.xlabel('X(AU)')
	plt.ylabel('Y(AU)')
	plt.rc('text',usetex = True)
	plt.rc('font',**{'sans-serif':'Arial','family':'sans-serif'})
	plt.title(r'\raggedright{\textit{'+title+'}}')
#end

#begin

p1 = Planeta('estrela 1',2.,1.,0,0,np.pi)#red
p2 = Planeta('estrela 2',2,-6.,0,0,np.pi)#blue
p3 = Planeta('estrela 3',2,3.,0.1,-np.pi/2,np.pi)#green

tmax = 20
t=np.arange(0,tmax,dt)

px_e1=np.zeros(t.size)
py_e1=np.zeros(t.size)
pvx_e1=np.zeros(t.size)
pvy_e1=np.zeros(t.size)

px_e2=np.zeros(t.size)
py_e2=np.zeros(t.size)
pvx_e2=np.zeros(t.size)
pvy_e2=np.zeros(t.size)

px_e3=np.zeros(t.size)
py_e3=np.zeros(t.size)
pvx_e3=np.zeros(t.size)
pvy_e3=np.zeros(t.size)

px_e1[0],py_e1[0],pvx_e1[0],pvy_e1[0] = p1.x,p1.y,p1.vx,p1.vy
px_e2[0],py_e2[0],pvx_e2[0],pvy_e2[0] = p2.x,p2.y,p2.vx,p2.vy
px_e3[0],py_e3[0],pvx_e3[0],pvy_e3[0] = p3.x,p3.y,p3.vx,p3.vy

m_s= GM

for i in range(t.size):
	p1.move(p2.x+p3.x,p2.y+p3.y,p2.vx+p3.vx,p2.vy+p3.vy,p2.m+p3.m,m_s)
	p2.move(p1.x+p3.x,p1.y+p3.y,p1.vx+p3.vx,p1.vy+p3.vy,p1.m++p3.m,m_s)
	p3.move(p1.x+p2.x,p1.y+p2.y,p1.vx+p2.vx,p1.vy+p2.vy,p1.m+p2.m,m_s)
	
	px_e1[i],py_e1[i],pvx_e1[i],pvy_e1[i] = p1.x,p1.y,p1.vx,p1.vy
	px_e2[i],py_e2[i],pvx_e2[i],pvy_e2[i] = p2.x,p2.y,p2.vx,p2.vy
	px_e3[i],py_e3[i],pvx_e3[i],pvy_e3[i] = p3.x,p3.y,p3.vx,p3.vy

fig = plt.figure(figsize=(6,5),facecolor='white')

'''plt.plot(px_e1,py_e1,'r-',lw = 1)
plt.plot(px_e2,py_e2,'b-',lw = 1)
plt.plot(px_e3,py_e3,'g-',lw = 1)'''

planeta = plt.axes(xlim=(1.1*min(px_e1+px_e2+px_e3),1.1*max(px_e1+px_e2+px_e3)),ylim=(1.1*min(py_e1+py_e2+py_e3),1.1*max(py_e1+py_e2+py_e3)),aspect = 'equal')
grafico(r'Gravita\c{c}\~ao com 3 corpos',True)

line1,=planeta.plot([],[],'r-',lw = 1)
line2,=planeta.plot([],[],'b-',lw = 1)
line3,=planeta.plot([],[],'g-',lw = 1)

def init():
	
	line1.set_data([],[])
	line2.set_data([],[])
	line3.set_data([],[])
	return line1,line2,line3,

#funcao animacao
def animate(i):
	#Adicinar rastro
	#imin = 0 if i < 100 else i - 100 #rastro de 10 posições
	#vet = rastro[imin:i+1]
	
	b = px_e1[:i]
	c = py_e1[:i]
	d = px_e2[:i]
	e = py_e2[:i]
	f = px_e3[:i]
	g = py_e3[:i]
	
	line1.set_data(b,c)
	line2.set_data(d,e)
	line3.set_data(f,g)
	return line1,line2,line3,
	
#cria animacao
anim = animation.FuncAnimation(fig,animate,init_func = init, frames=t.size,interval=0,blit=True,repeat = False)
anim.save('gravitacao_3_corpos.mp4', fps =120 , extra_args = ['-vcodec','libx264'] )

plt.show()

print 'concluido'