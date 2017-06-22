#_*_ coding: utf-8 _*_
#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

class Planeta():
	def __init__(self,massa,x,y,vx,vy):
		self.m = massa
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy
		self.e = 0.5*massa*(x**2+y**2) - (GM*self.m)/self.ratio(x,y)
	def ratio(self,x,y):
		return np.sqrt(x**2+y**2)
	def move(self):
		a_xt = -(GM/(self.ratio(self.x,self.y)**3))*self.x
		self.x = self.x + self.vx*dt+0.5*a_xt*dt**2
		self.vx = self.vx + a_xt*dt
	
		a_yt = -(GM/(self.ratio(self.x,self.y)**3))*self.y
		self.y = self.y + self.vy*dt+0.5*a_yt*dt**2
		self.vy = self.vy + a_yt*dt
		self.e = 0.5*self.m*(self.x**2+self.y**2) - (GM*self.m)/self.ratio(self.x,self.y)
		
#end

def grafico(_tlist,_dlist,title,xLabel,yLabel,_cor,visivel):
	fig = plt.figure(figsize=(4,4),facecolor='white')
	axes = plt.gca()
	plt.axes().set_aspect('equal','datalim')
	axes.axes.get_xaxis().set_visible(visivel)
	axes.yaxis.grid(True)
	axes.xaxis.grid(True)
	axes.spines['top'].set_color('none')
	axes.spines['right'].set_color('none')
	axes.yaxis.set_ticks_position('left')
	axes.xaxis.set_ticks_position('bottom')
	axes.spines['bottom'].set_position(('data',0))
	axes.spines['left'].set_position(('data',0))
	plt.rc('text',usetex = True)
	plt.rc('font',**{'sans-serif':'Arial','family':'sans-serif'})
	plt.xlabel(r'\raggedright{\textit{'+xLabel+'}}')
	plt.ylabel(r'\raggedright{\textit{'+yLabel+'}}')
	plt.title(r'Excentricidade com o aumento da velocidade',fontsize = 12)
	plt.plot(_tlist,_dlist,_cor,label = title)
	plt.legend(loc = 'upper right')
	plt.savefig('excentricidade',dpi=96)
	plt.show()
#end 

#begin

GM=4*np.pi**2
dt=0.001
k= 0
ex=[0]
acres=[0]
	
while k<4 :
	
	p1 = Planeta(1.,1,0,0,2*np.pi+k)
	tmax= 4
	t=np.arange(0,tmax,dt)
	x=np.zeros(t.size)
	y=np.zeros(t.size)
	vx=np.zeros(t.size)
	vy=np.zeros(t.size)
	e=np.zeros(t.size)
	
	x[0],y[0],vx[0],vy[0],e[0]=p1.x,p1.y,p1.vx,p1.vy,p1.e
	
	for i in range(t.size):
		p1.move()
		x[i],y[i],vx[i],vy[i],e[i]=p1.x,p1.y,p1.vx,p1.vy,p1.e
		
	a=max(x)
	b=min(x)
		
	if a<0 :
		a=-1*a
	elif b<0 :
		b=-1*b
		
	ex.append(np.sqrt(1-min(a,b)**2/max(a,b)**2))
	acres.append(k)
	k=k+0.1

grafico(acres, ex,'excentricidade','X (AU)','Y (AU)','r.',True)
	
print 'concluido'
#end

