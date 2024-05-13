# -*- coding: utf-8 -*-
"""
Modified on Sun Jul 16 18:50:23 2023

@author: Sanjana Balaji Kuttae
Supervised by: Prof. Dr. Volkhard Helms
Simulation kinetics based on :
1. J. Hennemann, R. S. Iwasaki, T. N. Grund, R. P. Diensthuber, F. Richter, A. Möglich, ChemBioChem 2018, 19, 1296
2. Ohlendorf R, Vidavski RR, Eldar A, Moffat K, \nMöglich A. From dusk till dawn: one-plasmid \nsystems for
   light-regulated gene expression. J Mol Biol. 2012 Mar 2;416(4):534-42. doi: 10.1016/j.jmb.
   2012.01.001. Epub 2012 Jan 8. Erratum in: J Mol\n Biol. 2014 Jan 24;426(2):500. PMID: 22245580.

"""


### Required Headers

from tkinter import *
from tkinter import ttk
import time
from tkinter import messagebox
from pdawn_variants import plot_graph

# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler


################################################################

#Creating a base Tkinter window and configuring the grid

root = Tk()
root.title("pDawn Variants Circuit")
root.resizable(False, False)
root.geometry("1200x700")
root.config(bg="lavender")
root.grid_rowconfigure(1, weight=0)
root.grid_columnconfigure(1, weight=1)


###################################################################################################

#Initial conditions 
#Default paramters for Initial parameters, Rate constants and Simulation parameters

default_init_parameters = [1, 0, 0, 1, 0, 1, 0, 0, 0]
default_rate_parameters = ['1/60', '15/60', '0.00012/60', 35, '2/60', 0.02, '1/3600', 1, '0.00001', 1, 3.7e-4, '0.688/60']
default_sim_parameters = [130, 14400+43200, 14400, 43200]
simulation_parameters = []

###################################################################################################
# Function to clear all the user inputs
def reset_button(resetlist):
    for i in resetlist:
        i.delete(0, 'end')

###################################################################################################

#Function to validate if the inputs are not entered or missing

def input_validation(lista):
   validity = True
   msg = "The input text is correct"
   for i in lista:
       if(i.get() == ''):
           msg = "Some inputs are missing"
           messagebox.showinfo('message', msg)
           validity= False
           break
       else:
            validity = True
   return validity


###################################################################################################

# Function to validate if the inputs are missing in any one of the input sections and then run the simulation
    
def validate_run(initlist, ratelist, simlist):
    if(input_validation(initlist) == False or input_validation(ratelist) == False or input_validation(simlist) == False):
        answer = messagebox.askretrycancel("pDawn Variants GUI", "Set missing parameters or close?")
        if(answer == False):
            
            root.destroy()
    else:
        runSimulation()
            
###################################################################################################    

#Funtion to validate if the user input is only numbers or allowed special characters
def validate_entry(new_text):
    checks = []
    for char in new_text:

        if char in new_text:
            checks.append(char == "/" or char == "." or char == "-" or char.isdecimal())
   
    return all(checks)


###################################################################################################

# Function to destroy or close the message pop up


def close_eq_pop(option):
	pop.destroy()

###################################################################################################

	
def viewEquation():
    global pop
    pop = Toplevel(root)
    pop.title("Equations")
    pop.geometry("1000x1000")

    pop_label = Label(pop, text= "1. d[YDD]/dt = -2kI*I[YDD]+k_R([YLD]+[YDL])\n"
                                      "\n2. d[YLD]/dt = -(kR+kI*I)[YLD]+kI*I[YDD]+kR[YLL]\n"
                                      "\n3. d[YDL]/dt = -(kR+kI*I)[YDL]+kI*I[YDD]+kR[YLL]\n"
                                      "\n4. d[YLL]/dt = -2kR[YLL]+kI*I([YLD]+[YDL])\n"
                                      
                                      "\n5. d[J]/dt =-kK[YDD][J]+kH[JP]+kP([YLD]+[YDL]+[YLL])[JP]\n"
                                      "\n6. d[JP]/dt = kK[YDD][J]-kH[JP]-kP([YLD]+[YDL]+[YLL])[JP]\n"
                                                                       
                                      "\n7. d[\u03BB]/dt = kT[Jp]\u00b2 / (KJ + [Jp])\u00b2 – kCD[\u03BB]\n"
                                      "\n8. d[M]/dt = kT[Jp]\u00b2 / (KJ + [Jp]\u00b2)\n"
                                      "\n \t\t(or) \n"
                                      "\n9. d[M]/dt = kT[Jp]\u00b2 / (KJ + [Jp]\u00b2) – kMD[M] \n"
                                      "\n10. d[R]/dt = k\u03BB K\u03BB / (K\u03BB + [\u03BB]\u2074) – kRD[M][R]", font=("helvetica", 11), anchor = "w", justify = "left")
    
    my_frame = Frame(pop)
    my_frame.grid(row=0, column=0)
    
    pop_label.grid(padx=10, pady=10)
    my_frame = Frame(pop)
    my_frame.grid(pady=5)

    yes = Button(my_frame, text="OK", command=lambda: close_eq_pop("ok"))
    yes.grid(row=0, column=1, padx=10)

###################################################################################################	
#Funtion to validate empty inputs and assign new input parameters into the pDawn_variants.py program 
    
def set_simulation_parameters():
    simulation_parameters.clear()
    if(whichbutton == "b1" and len(simulation_parameters) == 0):
        simulation_parameters.extend(["YDD_0="+ f"{s1value.get()}","YLD_0="+ f"{s2value.get()}", "YDL_0="+ f"{s2value.get()}","YLL_0="+ f"{s3value.get()}",
                                      "J_0="+ f"{s4value.get()}","JP_0="+ f"{s5value.get()}","P_0="+ f"{s6value.get()}", "L_0="+ f"{s7value.get()}",
                                      "M_0="+ f"{s8value.get()}", "R_0="+ f"{s9value.get()}"])
    elif(whichbutton == "b2" and len(simulation_parameters) == 0):
        simulation_parameters.extend(["kK="+ f"{r1value.get()}","kP="+ f"{r2value.get()}", "kI="+ f"{r3value.get()}","KJ="+ f"{r4value.get()}",
                                      "kCD="+ f"{r5value.get()}","Kλ="+ f"{r6value.get()}","kH="+ f"{r7value.get()}", "kT="+ f"{r8value.get()}",
                                      "kRD="+ f"{r9value.get()}", "kλ="+ f"{r10value.get()}", "km1="+ f"{r11value.get()}", "kMD="+ f"{r12value.get()}"])
    elif(whichbutton == "b3" and len(simulation_parameters) == 0):
        simulation_parameters.extend(["I="+ f"{intensityvalue.get()}","TMAX="+ f"{simulationvalue.get()}","LITE=" + f"{lightvalue.get()}","DARK="+f"{darkvalue.get()} "])
   
    with open('pdawn_variants.py') as file:
        lines = file.readlines()
        with open('pdawn_variants.py', 'w')as file:
            for num, i in enumerate (lines, 0):
                for j in simulation_parameters:
                    a = i.replace(" ", "")
                    if (a.split('=')[0] == j.split('=')[0] and j.split("=")[1] != ""):
                        a = j+'\n'
                        file.write(a)
                        break
                else:
                    file.write(lines[num])
                       
###################################################################################################   
#Function to capture which button was clicked in the GUI


def buttonclicked(buttonname):
    global whichbutton
    whichbutton = buttonname
    print(whichbutton)


###################################################################################################
#Function to reset the input fields to default values

def resetToDefault():
    if whichbutton == "bs1":
        defaultlist = default_init_parameters
        namelist = init_par
    elif whichbutton == "bs2":
        defaultlist = default_rate_parameters
        namelist = rate_par
    else:
        defaultlist = default_sim_parameters
        namelist =  sim_par
        for i in sim_par:
            print(i)
    for num, i in enumerate(defaultlist, 0):
        namelist[num].delete(0, 'end')
        namelist[num].insert(0,defaultlist[num])


###################################################################################################
#Function to run the simulation and plot the graphs

def runSimulation():
    print("Simulating......")
    titlelabel = Label(r_frame, text="Simulating........",relief=RAISED, fg="black", bg ="gray80")
    titlelabel.grid(row=10, column=0)
    #time.sleep(10)
    print("Simulation Finished.")
    titlelabel = Label(r_frame, text="Simulation Finished",relief=RAISED, fg="black", bg ="gray80")
    titlelabel.grid(row=15, column=0)
    
    execfile('pdawn_variants.py')
    plot_graph()


###################################################################################################
#Creating the main canvas on the root window

canvas = Canvas(root, width=2000, height=40, bg="lightgrey")
canvas.place(x=0, y=0)  
canvas.create_text(600, 20, text="pDawn Variants Simulation Tool", fill="darkblue", font=('Helvetica 13 bold'))        

######################################################################################################
# Creating the left canvas to insert the left frame

canvasl = Canvas(root, scrollregion = "0 0 1100 750", width = 835, height = 700)
canvasl.grid(row=0, column=0, sticky="news", padx=5, pady=50)


#Creating a vertical scroll for the left canvas
vsb = Scrollbar(root, orient="vertical", command=canvasl.yview)
vsb.grid(row=0, column=3, sticky='ns', pady=40)
canvasl.configure(yscrollcommand=vsb.set)

#Creating the left fram to insert the input fields

l_frame  =  Frame(canvasl,  width=500,  height=  900,  highlightbackground='grey',highlightthickness=1, bg='lightgrey')

l_frame.grid(row=1,  column=0,  padx=10,  pady=10,  sticky='w')

item = canvasl.create_window((2,2), anchor = NW,  window = l_frame )

########################################################################################################
# Creating the right canvas to display GUI information and run button

canvasr = Canvas(root, width = 930, height = 700, bg="lightgray")
canvasr.grid(row=0, column=1, sticky="news", padx=5, pady=50)

#Creating the right frame to display the run, viwe equation and reset all buttons
r_frame  =  Frame(canvasr,  width=400,  height=  900, bg="lightgray")
r_frame.grid(row=1,  column=4,  padx=10,  pady=10, sticky='ne')


titlelabel = Label(r_frame, text="About pDawn Variants GUI",relief=RAISED, fg="black", bg ="gray80")

titlelabel.grid(row=1, column=0, padx=20)


#####################################################################################################################################################
#Initial concentration Frame with respected labels and entry fields
init_frame  =  Frame(l_frame,  width=200,  height=  400,  highlightbackground='grey',highlightthickness=1,bg='lightgrey')
init_frame.grid(row=1,  column=0,  padx=10,  pady=10,  sticky='w')

titlelabel = Label(init_frame, text="Initial Concentration of Species",relief=RAISED, fg="black", bg ="gray80")
titlelabel.grid(row=1, column=0, sticky='ew', columnspan=2)


s_1 = Label(init_frame, text="Initial Concentration of YF1 with its two LOV photosensors in dark state", font='Helvetica 8 bold',  bg='lightgrey')
s_2 = Label(init_frame, text="Initial Concentration of YF1 with its two LOV photosensors in one in dark and the other in light state", font='Helvetica 8 bold',  bg='lightgrey')
s_3 = Label(init_frame, text="Initial Concentration of YF1 with its two LOV photosensors in light state", font='Helvetica 8 bold',  bg='lightgrey')
s_4 = Label(init_frame, text="Initial concentrations of a response regulator FixJ in dephosphorylated state", font='Helvetica 8 bold',  bg='lightgrey')
s_5 = Label(init_frame, text="Initial concentrations of a response regulator FixJ in phosphorylated state", font='Helvetica 8 bold',  bg='lightgrey')
s_6 = Label(init_frame, text="Amount of FixK2 promoter", font='Helvetica 8 bold',  bg='lightgrey')
s_7 = Label(init_frame, text="Initial concentration of cI lambda repressor", font='Helvetica 8 bold',  bg='lightgrey')
s_8 = Label(init_frame, text="Initial concentration of MF-Lon protease", font='Helvetica 8 bold',  bg='lightgrey')
s_9 = Label(init_frame, text="Initial concentration of TagRFP", font='Helvetica 8 bold',  bg='lightgrey')




s_1.grid(row=2, column=0, sticky='w')
s_2.grid(row=3, column=0, sticky='w')
s_3.grid(row=4, column=0, sticky='w')
s_4.grid(row=5, column=0, sticky='w')
s_5.grid(row=6, column=0, sticky='w')
s_6.grid(row=7, column=0, sticky='w')
s_7.grid(row=8, column=0, sticky='w')
s_8.grid(row=9, column=0, sticky='w')
s_9.grid(row=10, column=0, sticky='w')


s1value = StringVar()
s2value = StringVar()
s3value = StringVar()
s4value = StringVar()
s5value = StringVar()
s6value = StringVar()
s7value = StringVar()
s8value = StringVar()
s9value = StringVar()
    


#Entries for our form
s1entry = Entry(init_frame, textvariable=s1value,relief=GROOVE, validate="key",
                        validatecommand=(root.register(validate_entry), "%P"))

s2entry = Entry(init_frame, textvariable=s2value,relief=GROOVE,validate="key",
                        validatecommand=(root.register(validate_entry), "%P"))
                        
s3entry = Entry(init_frame, textvariable=s3value,relief=GROOVE, validate="key",
                        validatecommand=(root.register(validate_entry), "%P"))
                        
s4entry = Entry(init_frame, textvariable=s4value,relief=GROOVE, validate="key",
                        validatecommand=(root.register(validate_entry), "%P"))

s5entry = Entry(init_frame, textvariable=s5value,relief=GROOVE, validate="key",
                        validatecommand=(root.register(validate_entry), "%P"))

s6entry = Entry(init_frame, textvariable=s6value,relief=GROOVE, validate="key",
                        validatecommand=(root.register(validate_entry), "%P"))

s7entry = Entry(init_frame, textvariable=s7value,relief=GROOVE, validate="key",
                        validatecommand=(root.register(validate_entry), "%P"))

s8entry = Entry(init_frame, textvariable=s8value,relief=GROOVE, validate="key",
                        validatecommand=(root.register(validate_entry), "%P"))

s9entry = Entry(init_frame, textvariable=s9value,relief=GROOVE, validate="key",
                        validatecommand=(root.register(validate_entry), "%P"))

init_par = [s1entry, s2entry, s3entry, s4entry, s5entry, s6entry, s7entry, s8entry,s9entry]


titlelabel2 = Label(init_frame, text="symbol \t\t units",relief=RAISED, fg="black", bg ="gray80")
titlelabel2.grid(row=1, column=2, sticky='ew')

# aligning the entries
s1entry.grid(row=2, column=1)
s2entry.grid(row=3, column=1)
s3entry.grid(row=4, column=1)
s4entry.grid(row=5, column=1)
s5entry.grid(row=6, column=1)
s6entry.grid(row=7, column=1)
s7entry.grid(row=8, column=1)
s8entry.grid(row=9, column=1)
s9entry.grid(row=10, column=1)

unit_s1 = Label(init_frame, text="YDD_0 \t\t mol", font='Helvetica 8', bg='lightgrey')
unit_s2 = Label(init_frame, text="YLD_0,YDL_0 \t mol", font='Helvetica 8', bg='lightgrey')
unit_s3 = Label(init_frame, text="YLL_0 \t\t mol", font='Helvetica 8', bg='lightgrey')
unit_s4 = Label(init_frame, text="J_0 \t\t mol", font='Helvetica 8', bg='lightgrey')
unit_s5 = Label(init_frame, text="JP_0 \t\t mol", font='Helvetica 8', bg='lightgrey')
unit_s6 = Label(init_frame, text="P_0 \t\t mol", font='Helvetica 8', bg='lightgrey')
unit_s7 = Label(init_frame, text="L_0 \t\t mol", font='Helvetica 8', bg='lightgrey')
unit_s8 = Label(init_frame, text="M_0 \t\t mol", font='Helvetica 8', bg='lightgrey')
unit_s9 = Label(init_frame, text="R_0 \t\t mol", font='Helvetica 8', bg='lightgrey')

unit_s1.grid(row=2, column=2, sticky='w', padx=1)
unit_s2.grid(row=3, column=2, sticky='w', padx=1)
unit_s3.grid(row=4, column=2, sticky='w', padx=1)
unit_s4.grid(row=5, column=2, sticky='w', padx=1)
unit_s5.grid(row=6, column=2, sticky='w', padx=1)
unit_s6.grid(row=7, column=2, sticky='w', padx=1)
unit_s7.grid(row=8, column=2, sticky='w', padx=1)
unit_s8.grid(row=9, column=2, sticky='w', padx=1)
####################################################################################################################################################



#rate constants frame with respected lables and entry fields

rate_frame  =  Frame(l_frame,  width=400,  height=  400,  highlightbackground='grey',highlightthickness=1,bg='lightgrey')
rate_frame.grid(row=11,  column=0,  padx=10,  pady=0,  sticky='w')

titlelabel = Label(rate_frame, text="Rate Constants",relief=RAISED, fg="black", bg ="gray80")
titlelabel.grid(row=1, column=0, sticky='ew', columnspan=2)

titlelabel2 = Label(rate_frame, text="symbol \t\t units",relief=RAISED, fg="black", bg ="gray80")
titlelabel2.grid(row=1, column=2, sticky='ew')

r_1 = Label(rate_frame, text="Rate constant for phosphorylation", font='Helvetica 8 bold',  bg='lightgrey')
r_2 = Label(rate_frame, text="Rate constant for dephosphorylation ", font='Helvetica 8 bold',  bg='lightgrey')
r_3 = Label(rate_frame, text="Rate constants of photoactivation ", font='Helvetica 8 bold',  bg='lightgrey')
r_4 = Label(rate_frame, text="Dissociation constant of Phosphorylated FixJ to FixK2 promoter ", font='Helvetica 8 bold',  bg='lightgrey')
r_5 = Label(rate_frame, text="Degradation rate of cI lambda repressor by its C-terminal LVA tag", font='Helvetica 8 bold',  bg='lightgrey')
r_6 = Label(rate_frame, text="Dissociation constant of λ cI to pR promoter", font='Helvetica 8 bold',  bg='lightgrey')
r_7 = Label(rate_frame, text="Spontaneous hydrolysis of phosphorylated FixJ ", font='Helvetica 8 bold',  bg='lightgrey')
r_8 = Label(rate_frame, text="Transcription rate from Fixk2 promoter", font='Helvetica 8 bold',  bg='lightgrey')
r_9 = Label(rate_frame, text="Degradation rate of TagRFP by pdt#3 tag", font='Helvetica 8 bold',  bg='lightgrey')
r_10 = Label(rate_frame, text="Transcription rate from pR promoter", font='Helvetica 8 bold',  bg='lightgrey')
r_11 = Label(rate_frame, text="Rate constant for the dark recovery of YF1", font='Helvetica 8 bold',  bg='lightgrey')
r_12 = Label(rate_frame, text="Degradation rate of Mf-Lon protease by its C-terminal ASV tag ", font='Helvetica 8 bold',  bg='lightgrey')

r_1.grid(row=12, column=0, sticky='w')
r_2.grid(row=13, column=0, sticky='w')
r_3.grid(row=14, column=0, sticky='w')
r_4.grid(row=15, column=0, sticky='w')
r_5.grid(row=16, column=0, sticky='w')
r_6.grid(row=17, column=0, sticky='w')
r_7.grid(row=18, column=0, sticky='w')
r_8.grid(row=19, column=0, sticky='w')
r_9.grid(row=20, column=0, sticky='w')
r_10.grid(row=21, column=0, sticky='w')
r_11.grid(row=22, column=0, sticky='w')
r_12.grid(row=23, column=0, sticky='w')

r1value = StringVar()
r2value = StringVar()
r3value = StringVar()
r4value = StringVar()
r5value = StringVar()
r6value = StringVar()
r7value = StringVar()
r8value = StringVar()
r9value = StringVar()
r10value = StringVar()
r11value = StringVar()
r12value = StringVar()
    


#Entries for our form
r1entry = Entry(rate_frame, textvariable=r1value,relief=GROOVE, validate="key",
                        validatecommand=(root.register(validate_entry), "%P"))

r2entry = Entry(rate_frame, textvariable=r2value,relief=GROOVE,validate="key",
                        validatecommand=(root.register(validate_entry), "%P"))
                        
r3entry = Entry(rate_frame, textvariable=r3value,relief=GROOVE, validate="key",
                        validatecommand=(root.register(validate_entry), "%P"))
                        
r4entry = Entry(rate_frame, textvariable=r4value,relief=GROOVE, validate="key",
                        validatecommand=(root.register(validate_entry), "%P"))

r5entry = Entry(rate_frame, textvariable=r5value,relief=GROOVE, validate="key",
                        validatecommand=(root.register(validate_entry), "%P"))

r6entry = Entry(rate_frame, textvariable=r6value,relief=GROOVE, validate="key",
                        validatecommand=(root.register(validate_entry), "%P"))

r7entry = Entry(rate_frame, textvariable=r7value,relief=GROOVE, validate="key",
                        validatecommand=(root.register(validate_entry), "%P"))

r8entry = Entry(rate_frame, textvariable=r8value,relief=GROOVE, validate="key",
                        validatecommand=(root.register(validate_entry), "%P"))

r9entry = Entry(rate_frame, textvariable=r9value,relief=GROOVE, validate="key",
                        validatecommand=(root.register(validate_entry), "%P"))

r10entry = Entry(rate_frame, textvariable=r10value,relief=GROOVE, validate="key",
                        validatecommand=(root.register(validate_entry), "%P"))

r11entry = Entry(rate_frame, textvariable=r11value,relief=GROOVE, validate="key",
                        validatecommand=(root.register(validate_entry), "%P"))

r12entry = Entry(rate_frame, textvariable=r12value,relief=GROOVE, validate="key",
                        validatecommand=(root.register(validate_entry), "%P"))

rate_par = [r1entry, r2entry, r3entry, r4entry, r5entry, r6entry, r7entry, r8entry, r9entry, r10entry, r11entry, r12entry]

# aligning the entries
r1entry.grid(row=12, column=1)
r2entry.grid(row=13, column=1)
r3entry.grid(row=14, column=1)
r4entry.grid(row=15, column=1)
r5entry.grid(row=16, column=1)
r6entry.grid(row=17, column=1)
r7entry.grid(row=18, column=1)
r8entry.grid(row=19, column=1)
r9entry.grid(row=20, column=1)
r10entry.grid(row=21, column=1)
r11entry.grid(row=22, column=1)
r12entry.grid(row=23, column=1)

#Units specification for rate constants

unit_r1 = Label(rate_frame, text="kK \t\t s\u207b"+"\u00B9", font='Helvetica 8', bg='lightgrey')
unit_r2 = Label(rate_frame, text="kP \t\t s\u207b"+"\u00B9", font='Helvetica 8', bg='lightgrey')
unit_r3 = Label(rate_frame, text="kI \t\t µW\u207b"+"\u00B9"+"cm\u00b2"+"s\u207b"+"\u00B9", font='Helvetica 8', bg='lightgrey')
unit_r4 = Label(rate_frame, text="KJ \t\t mol", font='Helvetica 8', bg='lightgrey')
unit_r5 = Label(rate_frame, text="kCD \t\t s\u207b"+"\u00B9", font='Helvetica 8', bg='lightgrey')
unit_r6 = Label(rate_frame, text="Kλ \t\t mol", font='Helvetica 8', bg='lightgrey')
unit_r7 = Label(rate_frame, text="kH \t\t s\u207b"+"\u00B9", font='Helvetica 8', bg='lightgrey')
unit_r8 = Label(rate_frame, text="kT \t\t s\u207b"+"\u00B9", font='Helvetica 8', bg='lightgrey')
unit_r9 = Label(rate_frame, text="kRD \t\t s\u207b"+"\u00B9", font='Helvetica 8', bg='lightgrey')
unit_r10 = Label(rate_frame, text="kλ \t\t s\u207b"+"\u00B9", font='Helvetica 8', bg='lightgrey')
unit_r11 = Label(rate_frame, text="kR \t\t s\u207b"+"\u00B9", font='Helvetica 8', bg='lightgrey')
unit_r12 = Label(rate_frame, text="kMD \t\t s\u207b"+"\u00B9", font='Helvetica 8', bg='lightgrey')


unit_r1.grid(row=12, column=2, sticky='w', padx=1)
unit_r2.grid(row=13, column=2, sticky='w', padx=1)
unit_r3.grid(row=14, column=2, sticky='w', padx=1)
unit_r4.grid(row=15, column=2, sticky='w', padx=1)
unit_r5.grid(row=16, column=2, sticky='w', padx=1)
unit_r6.grid(row=17, column=2, sticky='w', padx=1)
unit_r7.grid(row=18, column=2, sticky='w', padx=1)
unit_r8.grid(row=19, column=2, sticky='w', padx=1)
unit_r9.grid(row=20, column=2, sticky='w', padx=1)
unit_r10.grid(row=21, column=2, sticky='w', padx=1)
unit_r11.grid(row=22, column=2, sticky='w', padx=1)
unit_r12.grid(row=23, column=2, sticky='w', padx=1)


######################################################################################################################################################
#Simulation Parameters Frame with respective lables and entry fields
sim_frame  =  Frame(l_frame,  width=200,  height=  400,  highlightbackground='grey',highlightthickness=1, bg='lightgrey')
sim_frame.grid(row=24,  column=0,  padx=10,  pady=0,  sticky='w')

titlelabel = Label(sim_frame, text="Simulation setup",relief=RAISED, fg="black", bg ="gray80")
titlelabel.grid(row=1, column=0, sticky='ew', columnspan=2)

titlelabel2 = Label(sim_frame, text="symbol \t\t units",relief=RAISED, fg="black", bg ="gray80")
titlelabel2.grid(row=1, column=2, sticky='ew')

#Text for our form
light_intensity = Label(sim_frame, text="Light intensity", font='Helvetica 8 bold',  bg='lightgrey')
simulation_time = Label(sim_frame, text="Simulation time", font='Helvetica 8 bold',  bg='lightgrey')
light_interval = Label(sim_frame, text="Light interval", font='Helvetica 8 bold',  bg='lightgrey')
dark_interval = Label(sim_frame, text="Dark interval", font='Helvetica 8 bold',  bg='lightgrey')

# aligning the entries
light_intensity.grid(row=26, column=0, sticky='w')
simulation_time.grid(row=27, column=0, sticky='w')
light_interval.grid(row=28, column=0, sticky='w')
dark_interval.grid(row=29, column=0, sticky='w')



# Tkinter variable for storing entries
intensityvalue = StringVar()
simulationvalue = StringVar()
lightvalue = StringVar()
darkvalue = StringVar()



#Entries for our form
intensityentry = Entry(sim_frame, textvariable=intensityvalue,relief=GROOVE, validate="key",
                        validatecommand=(root.register(validate_entry), "%P"))

simulationentry = Entry(sim_frame, textvariable=simulationvalue,relief=GROOVE,validate="key",
                        validatecommand=(root.register(validate_entry), "%P"))
                        
lightentry = Entry(sim_frame, textvariable=lightvalue,relief=GROOVE, validate="key",
                        validatecommand=(root.register(validate_entry), "%P"))
                        
darkentry = Entry(sim_frame, textvariable=darkvalue,relief=GROOVE, validate="key",
                        validatecommand=(root.register(validate_entry), "%P"))

sim_par = [intensityentry, simulationentry, lightentry, darkentry]


intensityentry.grid(row=26, column=1)
simulationentry.grid(row=27, column=1)
lightentry.grid(row=28, column=1)
darkentry.grid(row=29, column=1)

unit_intensity = Label(sim_frame, text="I \t\t µW\u207b"+"\u00B9"+"cm\u207b"+"\u00b2", font='Helvetica 8', bg='lightgrey')
unit_simulation = Label(sim_frame, text="TMAX \t\t s", font='Helvetica 8 ', bg='lightgrey')
unit_light = Label(sim_frame, text="LITE \t\t s", font='Helvetica 8', bg='lightgrey')
unit_dark = Label(sim_frame, text="DARK \t\t s", font='Helvetica 8', bg='lightgrey')


unit_intensity.grid(row=26, column=2, sticky='w', padx=1)
unit_simulation.grid(row=27, column=2, sticky='w', padx=1)
unit_light.grid(row=28, column=2, sticky='w', padx=1)
unit_dark.grid(row=29, column=2, sticky='w', padx=1)




#########################################################################################################

#Text widget to display GUI information including the Author name, Supervisors and references

txt_output = Text(r_frame, height=17, width=43, font='Helvetica 10')
txt_output.grid(padx=0, pady=10)
txt_output.insert(END, "Author and GUI designer : Sanjana Balaji Kuttae\npDawn circuits based on the kinetics\nformulated by Prof. Andreas Moglich\n\n")
txt_output.insert(END, "Kinetic equations for new constructs formulted by \nSanjana Balaji Kuttae \n\n")
txt_output.insert(END, "Supervisors: Prof. Dr. Volkhard Helms and \n")
txt_output.insert(END, "Dr. Shrikrishnan Sankaran\n\n")
txt_output.insert(END, "References:\n\n")
txt_output.insert(END, "1. J. Hennemann, R. S. Iwasaki, T. N. Grund, R. P. Diensthuber, F. Richter, A. Möglich, ChemBioChem 2018, 19, 1296.\n\n")
txt_output.insert(END, "2. Ohlendorf R, Vidavski RR, Eldar A, Moffat K, \nMöglich A. From dusk till dawn: one-plasmid \nsystems for light-regulated gene expression. J Mol Biol. 2012 Mar 2;416(4):534-42. doi: 10.1016/j.jmb.\n2012.01.001. Epub 2012 Jan 8. Erratum in: J Mol\n Biol. 2014 Jan 24;426(2):500. PMID: 22245580.")

txt_output.configure(state="disabled")



#########################################################################################################

#Buttons to set Initial concentrations

b1 = ttk.Button(init_frame, text="set parameters",command=lambda:[input_validation(init_par),buttonclicked("b1"),set_simulation_parameters()]).grid(row=25, column=1)
# Button to set back default values
bs1= ttk.Button(init_frame,text="set to default", command =lambda:[buttonclicked("bs1"), resetToDefault(), set_simulation_parameters()]).grid(row=25, column=0, sticky='w')
br1 = ttk.Button(init_frame, text="Reset",command=lambda:reset_button(init_par)).grid(row=25, column=2)



#Buttons to set Rate constants
b2 = ttk.Button(rate_frame, text="set parameters", command=lambda:[input_validation(rate_par),buttonclicked("b2"),set_simulation_parameters()]).grid(row=25, column=1)
# Button to set back default values
bs2= ttk.Button(rate_frame,text="set to default", command =lambda:[buttonclicked("bs2"), resetToDefault(), set_simulation_parameters()]).grid(row=25, column=0, sticky='w')
br2 = ttk.Button(rate_frame, text="Reset",command=lambda:reset_button(rate_par)).grid(row=25, column=2)

#Buttons to set Simulation Parameters
b3 = ttk.Button(sim_frame, text="set parameters", command=lambda:[input_validation(sim_par), buttonclicked("b3"),set_simulation_parameters()]).grid(row=32, column=1)
# Button to set back default values
bs3= ttk.Button(sim_frame,text="set to default", command =lambda:[buttonclicked("bs3"), resetToDefault(), set_simulation_parameters()]).grid(row=32, column=0, sticky='w')
br3 = ttk.Button(sim_frame, text="Reset",command=lambda:reset_button(sim_par)).grid(row=32, column=2)

#Button to view Kinetic equations
my_button = Button(r_frame, text="View Equation", command=viewEquation)
my_button.grid(row=33, column=0)

#Buttons to set Simulation Parameters
b_run = ttk.Button(r_frame, text="Run Simulation", command=lambda:[validate_run(init_par, rate_par, sim_par)]).grid(pady=20, row=33, column=0, sticky='e')

b3_run = ttk.Button(r_frame, text="Reset All", command=lambda:[reset_button(init_par), reset_button(rate_par), reset_button(sim_par)]).grid(pady=20, row=33, column=0, sticky='w')

#######################################################################



root.mainloop()
