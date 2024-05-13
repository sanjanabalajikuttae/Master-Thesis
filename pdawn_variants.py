#!/usr/bin/python

'''
simulate pDusk expression
by A.M. 2014 (Matlab), 2017 (ported to Python), 2022 (python 3)

v2: introduce KJ for promotor binding
v3.0 Modify the kinetics to support pDawn

Modified by Sanjana Balaji Kuttae
Email: kbsanjana@gmail.com

'''

import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

matplotlib.style.use('ggplot')

from tkinter import *
#####################################################

#Condition to 

# USE_FIT_VALUES = False
#NOCYCLES = 3
LITE=14400
DARK=43200 
TMAX=57600
AXLIMIT = [0, TMAX]




#####################################################  

#set and initial parameters for ODE simulation
tsteps=10001
tmin=0
tmax=TMAX

num_species=9

lite=LITE     # duration of the light cycle
dark=DARK     # duration of the dark cycle

I=130

# define species
YDD_0=1
YLD_0=0
YDL_0=0
YLL_0=0

J_0=1
JP_0=0


P_0=1
L_0=0
M_0=0
R_0=0

# define rates
kI=0.00012/60
kK=1/60
kP=15/60
KJ=35
klambda=1               #basal transcription rate
Klambda=0.02




#kI=0.000002             # k1 = kI * intensity
# km1=60*0.5*1/1142.          # dark recovery per second
km1=0.00037

kK_dd=kK                 # phosphorylation rates
kK_ld=0
kK_dl=0
kK_ll=0

kP_dd=0                  # dephosphorylation rates
kP_ld=kP
kP_dl=kP
kP_ll=kP

kH=1/3600
kT=1
# kdeg=0.37    
#kRD=0.047/60
kRD=0.00001
kCD=2/60
kMD=0.688/60
#kMD=0
pR_basal=0


########################################################################################################

#setup initial conditions
X0=[YDD_0,YLD_0,YDL_0,YLL_0,J_0,JP_0,L_0,M_0,R_0]

#setup time vector
t=np.linspace(tmin,tmax,tsteps)

# the ODE system
def pDusk(y,t,kI,km1,kK_dd,kH,kP_dl,kP_ld,kP_ll,kT,klambda,Klambda,KJ,dark,lite,I):
  # check whether we are in dark or light period
  tcycle=t-(dark+lite)*np.floor(t/(dark+lite))
  # if (tcycle<=dark):
  #   k1=0
  # else:
  #   k1=kI*I
  if (tcycle<=lite):
    k1=kI*I
  else:
    k1=0
  
  # define differential equations
  dy=np.linspace(0,0,9)
  # YDD
  dy[0]=(-2*k1*y[0]+km1*(y[1]+y[2]))
  # YLD
  dy[1]=(k1*y[0]-(km1+k1)*y[1]+km1*y[3])
  # YLD
  dy[2]=(k1*y[0]-(km1+k1)*y[2]+km1*y[3])
  # YLL
  dy[3]=(k1*(y[1]+y[2])-2*km1*y[3])
  
  # J
  dy[4]=(-kK_dd*y[0]*y[4]+(kH+kP_dl*y[1]+kP_ld*y[2]+kP_ll*y[3])*y[5])
  # JP
  dy[5]=(kK_dd*y[0]*y[4]-(kH+kP_dl*y[1]+kP_ld*y[2]+kP_ll*y[3])*y[5])
  
  #cI
  dy[6]=((kT*y[5]**2)/(KJ+y[5]**2)-kCD*y[6])
  #mflon
  dy[7]=((kT*y[5]**2/(KJ+y[5]**2))-kMD*y[7])
  # R
  dy[8]=((klambda*Klambda)/(Klambda+y[6]**4)-kRD*y[7]*y[8])
    
  return dy

# now do the actual integration
args=(kI,km1,kK_dd,kH,kP_dl,kP_ld,kP_ll,kT,klambda,Klambda,KJ,dark,lite,I)
z = integrate.odeint(pDusk, X0, t, args=args)


#####################################################  
#Function to plot the graphs in a new window with navigation and export options



def plot_graph():
    # plot results
    root = Tk()
    root.wm_title("pDawn Variants Plots")
    root.geometry("600x700")
    # the figure that will contain the plot
    fig = Figure(figsize = (5, 5), dpi = 150)
    
    t1 = t/3600
    
    fig, ax = plt.subplots()
    ax.plot(t1,z[:,0], color='black', linewidth=1.5, label = 'YDD')
    ax.plot(t1,z[:,1], color='orange', linewidth=1.5, label = 'YLD')
    ax.plot(t1,z[:,2], color='orange', linewidth=1.5, label = 'YDL')
    ax.plot(t1,z[:,3], color='darkblue', linewidth=1.5, label = 'YLL')
    ax.plot(t1,z[:,4], color='green', linewidth=1.5, label = 'FixJ')
    ax.plot(t1,z[:,5], color='grey', linewidth=1.5, label = 'FixJ-P')
    
    
    plt.xlabel(r'$Time$ [hr]')
    plt.ylabel(r'$Species$ [mol]')
    plt.xlim(0, )
    
    # Create a legend outside the plot
    legend = ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize = 12)
    fig.tight_layout()
    

    canvas1 = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    
    toolbar1 = Frame(master=root)
    toolbar1.pack(side=TOP, fill=BOTH)
    toolbar1 = NavigationToolbar2Tk(canvas1, toolbar1)

    #to adjust the horizontal position of the graph. 0.9 refers to left margin close to the right margin - thinner graph
    plt.subplots_adjust()

    # draw patches to indicate dark/light cycle
    [ymin,ymax]=plt.ylim()
    
    ax=plt.gca()
    t_period=lite+dark
    t_current=0
    t1_current = 0
    t1max = tmax/3600
    lite1=lite/3600
    dark1=dark/3600
    while (t1_current<tmax):
      patchli=patches.Rectangle((t1_current,ymin),lite1,ymax-ymin,edgecolor='none',facecolor=[0,0,0.9,0.2])
      # patchli=patches.Rectangle((t_current+dark,ymin),lite,ymax-ymin,edgecolor='none',facecolor=[0,0,0.9,0.2])
      # patchli=patches.Rectangle((t_current+dark,ymin),lite,ymax-ymin,edgecolor='none',facecolor=[0,0,0.9,0.2])
      ax.add_patch(patchli)
      t_current+=t_period
      t1_current = t_current/3600
    
    
      
    # plot tagRFP production
    
    fig1 = Figure(figsize = (5, 5), dpi = 150)    
    t1 = t/3600
    # plt.figure()
    fig1, ax1 = plt.subplots(1)
    ax1.plot(t1,z[:,-1], color='red', linewidth=1.5, label = 'TagRFP')
    ax1.plot(t1,z[:,-2], color='green', linewidth=1.5, label = 'Mf-Lon ')
    ax1.plot(t1,z[:,-3], color='orange', linewidth=1.5, label = 'cI') 
    legend = ax1.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize = 12)
    fig1.tight_layout()
    
    
    canvas2 = FigureCanvasTkAgg(fig1, master=root)  # A tk.DrawingArea.
    canvas2.draw()
    canvas2.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
    
    
    
    toolbar2 = Frame(master=root)
    toolbar2.pack(side=BOTTOM, fill=BOTH)
    toolbar2 = NavigationToolbar2Tk(canvas2, toolbar2)
    

    plt.xlabel(r'$Time$ [hr]')
    plt.ylabel(r'$cI,\ Mf-Lon,\ TagRFP$') 
    plt.xlim(0, )
    # draw patches to indicate dark/light cycle
    [ymin,ymax]=plt.ylim()
    
    ax=plt.gca()
    t_period=lite+dark
    t_current=0
    t1_current = 0
    t1max = tmax/3600
    lite1=lite/3600
    dark1=dark/3600
    while (t1_current<tmax):
      patchli=patches.Rectangle((t1_current,ymin),lite1,ymax-ymin,edgecolor='none',facecolor=[0,0,0.9,0.2])
      # patchli=patches.Rectangle((t_current+dark,ymin),lite,ymax-ymin,edgecolor='none',facecolor=[0,0,0.9,0.2])
      ax.add_patch(patchli)
      t_current+=t_period
      t1_current = t_current/3600


    root.mainloop()


# report actual rates

namestr = ['kI', 'kK', 'kP', 'KJ', 'klambda', 'Klambda', 'Lambda']
for index, entry in enumerate([kI, kK, kP, KJ, klambda, Klambda, L_0]):
   print(namestr[index], entry)

# export data
export=np.vstack((t,z.transpose()))
export=export.transpose()
plot_graph()