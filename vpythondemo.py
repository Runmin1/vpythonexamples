from __future__ import division, print_function
from visual import *
import wx

L = 320
d = 20
offset = 15

myWindow = window(title='Spring Energy Simulation', width=L*3, height=L*2)
myPanel = myWindow.panel
wx.StaticText(myPanel, pos=(d,4), size=(L-2*d,d), label='Displayed below is the spring energy simulator:', style=wx.ALIGN_CENTRE)
myDisplay = display(window=myWindow, x=offset, y=offset*2, width=L*2, height=L*1.75)

# Constants
g = 9.8
mball = 0.5
L0 = 0.3
ks = 12
deltat  = 1e-1
speed = 10

t = 0 # Start counting time at zero

def updateG(evt):
    global g
    newG = gEntry.GetValue()
    try:
        g = float(newG)
    except ValueError:
        pass
    
def updateMBall(evt):
    global mball
    newMBall = mBallEntry.GetValue()
    try:
        mball = float(newMBall)
    except ValueError:
        pass

def updateL0(evt):
    global L0
    newL0 = Lentry.GetValue()
    try:
        L0 = float(newL0)
    except ValueError:
        pass

def updateKS(evt):
    global ks
    newKS = ksEntry.GetValue()
    try:
        ks = float(newKS)
    except ValueError:
        pass

def updateSpeed(evt):
    global speed
    speed = speedEntry.GetValue()

textBoxDims = (100,15)
labelPosX = L*2.1
boxPosX = L*2.4

# Initializing input fields for constants
wx.StaticText(myPanel, pos=(labelPosX, 90), label='Gravity', style=wx.ALIGN_CENTRE)
gEntry = wx.TextCtrl(myPanel, pos=(boxPosX, 90),value=str(g), size=textBoxDims, style=wx.TE_PROCESS_ENTER)
gEntry.Bind(wx.EVT_TEXT_ENTER, updateG)

wx.StaticT≡jedi=0, ext(myPanel, pos=(l≡ (*args, ***kwargs*) ≡jedi≡abelPosX, 110), label='Mass of ball', style=wx.ALIGN_CENTRE)
mBallEntry = wx.TextCtrl(myPanel, pos=(boxPosX, 110), value=str(mball),
size=textBoxDims, style=wx.TE_PROCESS_ENTER)
mBallEntry.Bind(wx.EVT_TEXT_ENTER, updateMBall)

wx.StaticText(myPanel, pos=(labelPosX, 130), label='Relaxed length', style=wx.ALIGN_CENTRE)
Lentry = wx.TextCtrl(myPanel, pos=(boxPosX, 130), value=str(L0), size=textBoxDims, style=wx.TE_PROCESS_ENTER)
Lentry.Bind(wx.EVT_TEXT_ENTER, updateL0)

wx.StaticText(myPanel, pos=(labelPosX, 150), label='Spring constant', style=wx.ALIGN_CENTRE)
ksEntry = wx.TextCtrl(myPanel, pos=(boxPosX, 150), value=str(ks), size=textBoxDims, style=wx.TE_PROCESS_ENTER)
ksEntry.Bind(wx.EVT_TEXT_ENTER, updateKS)

wx.StaticText(myPanel, pos=(labelPosX, 190), label='Rendering speed', style=wx.ALIGN_CENTRE)
speedEntry = wx.Slider(myPanel, pos=(labelPosX, 210), size=(0.9*L, 20), minValue=50, maxValue=1e4)
speedEntry.SetValue(50)

## objects
ceiling = box(pos=vector(0,0,0), size = vector(0.2, 0.01, 0.2))         ## origin is at ceiling
ball = sphere(pos=vector(-0.2391,-0.2148,-0.0807), radius=0.025, color=color.orange) ## note: spring initially compressed
spring = helix(pos=ceiling.pos, color=color.cyan, thickness=.003, coils=40, radius=0.015) ## change the color to be your spring color
spring.axis = ball.pos - ceiling.pos

## initial values
ball.p = mball*vector(0,0,0)
vball = vector (0.319,-0.124,0.233)
## improve the display
scene.autoscale = 0             ## don't let camera zoom in and out as ball moves
scene.center = vector(0,-L0,0)   ## move camera down to improve display visibility

# Animations
trail = curve(color=ball.color) ## before the loop
fnetArrow = arrow(color=color.green)
pArrow = arrow(color=color.red)
scene.autoscale = False
scene.center = vector(0,-L0,0)   ## move camera down to improve display visibility

while True: # Keeps the display live after the loop has finished
    while t < 100:
        rate(speed)
        L = ball.pos - ceiling.pos
        magL = sqrt(L.x**2+L.y**2+L.z**2)
        Lhat = L/magL
        
        Fspring = ks*(magL-L0)
        Fs = -Fspring*Lhat
        Fgrav = vector(0,-g*mball,0)
        Fnet = Fs +Fgrav
        vball = vball + (Fnet/mball)*deltat
        pball = vball * mball
        ball.pos = ball.pos + (vball*deltat)
        
        spring.axis = ball.pos -ceiling.pos
        trail.append(pos=ball.pos)
         
        t = t + deltat
