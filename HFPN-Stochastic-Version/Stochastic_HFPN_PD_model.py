import os
import sys
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from sys import platform


cwd = os.getcwd() # Get current working directory
root_folder = os.sep + "HFPN-Stochastic-Version"
# Move to 'utils' from current directory position
sys.path.insert(0, cwd[:(cwd.index(root_folder)+len(root_folder))] + os.sep + "HFPN-Stochastic-Version" + os.sep)

# Import HFPN class to work with hybrid functional Petri nets
from stochastic_hfpn import HFPN


# Import initial token, firing conditions and rate functions
from PD_sHFPN_initial_tokens import *
from PD_sHFPN_rate_functions import *
from PD_sHFPN_firing_conditions import *
from PD_sHFPN_inputs import *
from visualisation import Analysis
# from AD_parameters import *
# from AD_rate_functions import *
# from AD_initial_tokens import *
# from AD_firing_conditions import *
# from AD_sHFPN_inputs import *

#Import GUI
import tkinter as tk
from tkinter import ttk
from functools import partial
import glob
from PIL import ImageTk,Image 
import webbrowser as webbrowser
from tkinter import font as tkfont

#Import Threading
import threading

#Make Windows Taskbar Show as MNG Icon
import ctypes
myappid = 'sHFPN GUI' # arbitrary string
if platform == 'win32':
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

#Important packages for Graph embedding
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
style.use("ggplot")

class sHFPN_GUI_APP:
    def __init__(self):
        self.root = tk.Tk()
        if platform == 'darwin':
            img = tk.Image("photo", file="mng.png")
            self.root.iconphoto(True, img)
        if platform == 'win32':
            self.root.iconbitmap(r'mngicon.ico')
        self.root.title("sHFPN GUI")
        self.root.geometry("800x660")
        self.Left_Sidebar()
        self.root.bind("<Control-l>", lambda x: self.hide())
        self.hidden=0
        
    def Left_Sidebar(self):
        self.frame1= tk.Frame(self.root, width=175)
        self.frame1.pack(side="left", fill=tk.BOTH)
        self.lb = tk.Listbox(self.frame1)
        self.lb['bg']= "black"
        self.lb['fg']= "lime"
        self.lb.pack(side="left", fill=tk.BOTH)
        
        #***Add Different Channels***

        self.lb.insert(tk.END, "PD Inputs","Run PD sHFPN","AD Inputs", "Run AD sHFPN", "Neuronal Healthbar", "Analysis", "Saved Runs", "About")
     
        
        #*** Make Main Frame that other frames will rest on:
        self.frame2= tk.Frame(self.root)
        self.frame2.pack(side="left", fill=tk.BOTH, expand=1)
        self.frame2.grid_rowconfigure(0, weight=1)
        self.frame2.grid_columnconfigure(0, weight=1)
        
        self.PD_Inputs_Page()
        self.Run_sHFPN_Page()
        self.AD_Inputs_Page()
        self.Run_AD_sHFPN_Page()        
        self.Neuronal_HealthBar()
        self.Analysis_page()
        self.show_saved_runs()
        self.About_Page()
        
        #***Callback Function to execute if items in Left_Sidebars are selected
        def callback(event):
            selection = event.widget.curselection()
            if selection:
                index=selection[0] #selection is a tuple, first item of tuple gives index
                item_name=event.widget.get(index)
                if item_name == "PD Inputs":
                    self.frame3.tkraise()
    
                if item_name == "Run PD sHFPN":
                    self.frame4.tkraise()
                    
                if item_name =="AD Inputs":
                    self.AD_frame3.tkraise()
                    
                if item_name == "Run AD sHFPN":
                    self.AD_frame1.tkraise()
                    
                if item_name == "Neuronal Healthbar":
                    self.frame8.tkraise()
                    
                if item_name == "Analysis":
                    self.frame5.tkraise()
                    
                if item_name == "Saved Runs":
                    #Destroy frame to update and remake frame.
                    self.frame6.destroy()
                    self.show_saved_runs()
                    self.frame6.tkraise()
                    
                if item_name == "About":
                    self.frame7.tkraise()
                    
                        
        self.lb.bind("<<ListboxSelect>>", callback)
        
        #***Select item in Listbox and Display Corresponding output in Right_Output
        #self.lb.bind("<<ListboxSelect>>", Lambda x: show)
 
    def make_scrollbar_sHFPN(self):
        self.canvas = tk.Canvas(self.frame4)
        self.canvas.pack(side="left", fill=tk.BOTH, expand=1)
        
        self.scrollbar = ttk.Scrollbar(self.frame4, orient=tk.VERTICAL, command =self.canvas.yview)
        self.scrollbar.pack(side="left", fill=tk.Y)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion= self.canvas.bbox("all")))
        
        #Create another frame inside the canvas
        self.frame_in_canvas = tk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.frame_in_canvas, anchor="nw")
        
        
    def make_scrollbar_AD_sHFPN(self):
        self.AD_canvas = tk.Canvas(self.AD_frame1)
        self.AD_canvas.pack(side="left", fill=tk.BOTH, expand=1)
        
        self.AD_scrollbar = ttk.Scrollbar(self.AD_frame1, orient=tk.VERTICAL, command =self.canvas.yview)
        self.AD_scrollbar.pack(side="left", fill=tk.Y)
        
        self.AD_canvas.configure(yscrollcommand=self.AD_scrollbar.set)
        self.AD_canvas.bind('<Configure>', lambda e: self.AD_canvas.configure(scrollregion= self.AD_canvas.bbox("all")))
        
        #Create another frame inside the canvas
        self.AD_frame_in_canvas = tk.Frame(self.AD_canvas)
        self.AD_canvas.create_window((0,0), window=self.AD_frame_in_canvas, anchor="nw")
        
        
    def make_scrollbar_Analysis(self):
        self.canvas2 = tk.Canvas(self.frame5)
        self.canvas2.pack(side="left", fill=tk.BOTH, expand=1)
        
        self.scrollbar2 = ttk.Scrollbar(self.frame5, orient=tk.VERTICAL, command =self.canvas2.yview)
        self.scrollbar2.pack(side="left", fill=tk.Y)
        
        self.canvas2.configure(yscrollcommand=self.scrollbar2.set)
        self.canvas2.bind('<Configure>', lambda e: self.canvas2.configure(scrollregion= self.canvas2.bbox("all")))
        
        #Create another frame inside the canvas2
        self.frame_in_canvas_Analysis = tk.Frame(self.canvas2)
        self.canvas2.create_window((0,0), window=self.frame_in_canvas_Analysis, anchor="nw")   
    
    def AD_make_scrollbar_Inputs_Page(self):
        self.AD_canvas3 = tk.Canvas(self.AD_frame3)
        self.AD_canvas3.pack(side="left", fill=tk.BOTH, expand=1)
        
        self.AD_scrollbar3 = ttk.Scrollbar(self.AD_frame3, orient=tk.VERTICAL, command =self.AD_canvas3.yview)
        self.AD_scrollbar3.pack(side="left", fill=tk.Y)
        
        self.AD_canvas3.configure(yscrollcommand=self.AD_scrollbar3.set)
        self.AD_canvas3.bind('<Configure>', lambda e: self.AD_canvas3.configure(scrollregion= self.AD_canvas3.bbox("all")))
        
        #Create another frame inside the canvas
        self.AD_frame3_in_canvas_Inputs = tk.Frame(self.AD_canvas3)
        self.AD_canvas3.create_window((0,0), window=self.AD_frame3_in_canvas_Inputs, anchor="nw")  
 
    def AD_Inputs_Page(self):
        self.AD_frame3=tk.Frame(self.frame2)
        #self.frame3.pack(side="left", fill=tk.BOTH,expand=1)
        self.AD_frame3.grid(row=0,column=0,sticky="nsew")
        self.AD_make_scrollbar_Inputs_Page()
        
        #Inputs Labels and Entry Boxes
        #*Run Save Name*
        self.Label_run_save_name = tk.Label(self.AD_frame3_in_canvas_Inputs, text="Run Save Name")
        self.Label_run_save_name.grid(row=0,column=0)
        self.Label_run_save_name_e = tk.Entry(self.AD_frame3_in_canvas_Inputs)
        self.Label_run_save_name_e.grid(row=0,column=1)
        self.Label_run_save_name_e.insert(tk.END, "sHFPN_Save_Name")
        #*Number of Timesteps*
        self.Label_no_timesteps = tk.Label(self.AD_frame3_in_canvas_Inputs, text="Number of Timesteps")
        self.Label_no_timesteps.grid(row=1,column=0)
        self.Label_no_timesteps_e = tk.Entry(self.AD_frame3_in_canvas_Inputs)
        self.Label_no_timesteps_e.grid(row=1,column=1)
        self.Label_no_timesteps_e.insert(tk.END, "50000")
        self.Label_Help_no_timesteps = tk.Label(self.AD_frame3_in_canvas_Inputs, text="Only input increments of 1000")
        self.Label_Help_no_timesteps.grid(row=1, column=2)
        #*Timestep Size*
        self.Label_timestep_size = tk.Label(self.AD_frame3_in_canvas_Inputs, text="Timestep Size (s)")
        self.Label_timestep_size.grid(row=2,column=0)
        self.Label_timestep_size_e = tk.Entry(self.AD_frame3_in_canvas_Inputs)
        self.Label_timestep_size_e.grid(row=2,column=1)
        self.Label_timestep_size_e.insert(tk.END, "0.001")
        
        #*SD Header*
        self.SD_font = tkfont.Font(family='Helvetica', size=10, weight="bold", slant="italic")
        self.Label_Header = tk.Label(self.AD_frame3_in_canvas_Inputs, text="Adjust Transition Stochasticity Levels", font=self.SD_font)
        self.Label_Header.grid(row=3, column=1, pady=20)
        
        #*CholSD*
        self.Label_CholSD = tk.Label(self.AD_frame3_in_canvas_Inputs, text="CholSD (0 to 1)")
        self.Label_CholSD.grid(row=4,column=0)
        self.Label_CholSD_e = tk.Entry(self.AD_frame3_in_canvas_Inputs)
        self.Label_CholSD_e.grid(row=4,column=1)
        self.Label_CholSD_e.insert(tk.END, "0.1")       
        
        #*Calcium Module SD*
        self.Label_Calcium = tk.Label(self.AD_frame3_in_canvas_Inputs, text="Calcium Module SD (0 to 1)")
        self.Label_Calcium.grid(row=5,column=0)
        self.Label_Calcium_e = tk.Entry(self.AD_frame3_in_canvas_Inputs)
        self.Label_Calcium_e.grid(row=5,column=1)
        self.Label_Calcium_e.insert(tk.END, "0.1")    
        
        #*Mutations Header*
        self.Mutations_Header = tkfont.Font(family='Helvetica', size=10, weight="bold", slant="italic") 
        self.Label_Header_Mutations = tk.Label(self.AD_frame3_in_canvas_Inputs, text="Mutations and Risk Factors", font=self.Mutations_Header)
        self.Label_Header_Mutations.grid(row=6, column=1)
        
        #*ApoE4 Mutation
        self.ApoE4_Mutation = tk.Label(self.AD_frame3_in_canvas_Inputs, text="ApoE4")
        self.ApoE4_Mutation.grid(row=7, column=0)
        self.ApoE4_var = tk.IntVar()
        self.ApoE4_Mutation_checkbox = tk.Checkbutton(self.AD_frame3_in_canvas_Inputs, variable=self.ApoE4_var)
        self.ApoE4_Mutation_checkbox.grid(row=7, column=1)

        #CD33 mutation
        self.CD33_Mutation = tk.Label(self.AD_frame3_in_canvas_Inputs, text="CD33")
        self.CD33_Mutation.grid(row=8, column=0)
        self.CD33_var = tk.IntVar()
        self.CD33_Mutation_checkbox = tk.Checkbutton(self.AD_frame3_in_canvas_Inputs, variable=self.CD33_var)
        self.CD33_Mutation_checkbox.grid(row=8, column=1)
            
         #Aged 
        self.Aged_risk = tk.Label(self.AD_frame3_in_canvas_Inputs, text="Aged")
        self.Aged_risk.grid(row=9, column=0)
        self.Aged_var = tk.IntVar()
        self.Aged_risk_checkbox = tk.Checkbutton(self.AD_frame3_in_canvas_Inputs, variable=self.Aged_var)
        self.Aged_risk_checkbox.grid(row=9, column=1)
                       
        
        
        def save_entry_inputs(self):
            self.HFPN_run_save_name =self.Label_run_save_name_e.get()
            self.HFPN_number_of_timesteps = self.Label_no_timesteps_e.get()
            self.HFPN_timestep_size = self.Label_timestep_size_e.get()
            self.HFPN_CholSD = self.Label_CholSD_e.get()
            self.HFPN_CalciumSD = self.Label_Calcium_e.get()
            print("Inputs Saved")
            self.button_1.config(state="normal", text="Run sHFPN")
            self.AD_button_1.config(state="normal", text="Run AD sHFPN")            
            self.button_6.config(state=tk.DISABLED)
            
        #*Save Inputs Button*
        self.button_6 = tk.Button(self.AD_frame3_in_canvas_Inputs, text = "Save Inputs", cursor="hand2", command=partial(save_entry_inputs, self))    
        self.button_6.grid(row=20, column=1, pady=20)  
        self.Label_Save_Inputs_Button_info = tk.Label(self.AD_frame3_in_canvas_Inputs, text="Double check your inputs")
        self.Label_Save_Inputs_Button_info.grid(row=20, column=2)        
        
    def make_scrollbar_Inputs_Page(self):
        self.canvas3 = tk.Canvas(self.frame3)
        self.canvas3.pack(side="left", fill=tk.BOTH, expand=1)
        
        self.scrollbar3 = ttk.Scrollbar(self.frame3, orient=tk.VERTICAL, command =self.canvas3.yview)
        self.scrollbar3.pack(side="left", fill=tk.Y)
        
        self.canvas3.configure(yscrollcommand=self.scrollbar3.set)
        self.canvas3.bind('<Configure>', lambda e: self.canvas3.configure(scrollregion= self.canvas3.bbox("all")))
        
        #Create another frame inside the canvas2
        self.frame_in_canvas_Inputs = tk.Frame(self.canvas3)
        self.canvas3.create_window((0,0), window=self.frame_in_canvas_Inputs, anchor="nw")   
    
    def PD_Inputs_Page(self):
        self.frame3=tk.Frame(self.frame2)
        #self.frame3.pack(side="left", fill=tk.BOTH,expand=1)
        self.frame3.grid(row=0,column=0,sticky="nsew")
        self.make_scrollbar_Inputs_Page()
        
        #Inputs Labels and Entry Boxes
        #*Run Save Name*
        self.Label_run_save_name = tk.Label(self.frame_in_canvas_Inputs, text="Run Save Name")
        self.Label_run_save_name.grid(row=0,column=0)
        self.Label_run_save_name_e = tk.Entry(self.frame_in_canvas_Inputs)
        self.Label_run_save_name_e.grid(row=0,column=1)
        self.Label_run_save_name_e.insert(tk.END, "sHFPN_Save_Name")
        #*Number of Timesteps*
        self.Label_no_timesteps = tk.Label(self.frame_in_canvas_Inputs, text="Number of Timesteps")
        self.Label_no_timesteps.grid(row=1,column=0)
        self.Label_no_timesteps_e = tk.Entry(self.frame_in_canvas_Inputs)
        self.Label_no_timesteps_e.grid(row=1,column=1)
        self.Label_no_timesteps_e.insert(tk.END, "50000")
        self.Label_Help_no_timesteps = tk.Label(self.frame_in_canvas_Inputs, text="Only input increments of 1000")
        self.Label_Help_no_timesteps.grid(row=1, column=2)
        #*Timestep Size*
        self.Label_timestep_size = tk.Label(self.frame_in_canvas_Inputs, text="Timestep Size (s)")
        self.Label_timestep_size.grid(row=2,column=0)
        self.Label_timestep_size_e = tk.Entry(self.frame_in_canvas_Inputs)
        self.Label_timestep_size_e.grid(row=2,column=1)
        self.Label_timestep_size_e.insert(tk.END, "0.001")
        
        #*SD Header*
        self.SD_font = tkfont.Font(family='Helvetica', size=10, weight="bold", slant="italic")
        self.Label_Header = tk.Label(self.frame_in_canvas_Inputs, text="Adjust Transition Stochasticity Levels", font=self.SD_font)
        self.Label_Header.grid(row=3, column=1, pady=20)
        
        #*CholSD*
        self.Label_CholSD = tk.Label(self.frame_in_canvas_Inputs, text="CholSD (0 to 1)")
        self.Label_CholSD.grid(row=4,column=0)
        self.Label_CholSD_e = tk.Entry(self.frame_in_canvas_Inputs)
        self.Label_CholSD_e.grid(row=4,column=1)
        self.Label_CholSD_e.insert(tk.END, "0.1")       
        
        #*Calcium Module SD*
        self.Label_Calcium = tk.Label(self.frame_in_canvas_Inputs, text="Calcium Module SD (0 to 1)")
        self.Label_Calcium.grid(row=5,column=0)
        self.Label_Calcium_e = tk.Entry(self.frame_in_canvas_Inputs)
        self.Label_Calcium_e.grid(row=5,column=1)
        self.Label_Calcium_e.insert(tk.END, "0.1")    
        
        #*Mutations Header*
        self.Mutations_Header = tkfont.Font(family='Helvetica', size=10, weight="bold", slant="italic") 
        self.Label_Header_Mutations = tk.Label(self.frame_in_canvas_Inputs, text="Mutations", font=self.Mutations_Header)
        self.Label_Header_Mutations.grid(row=6, column=1)
        
        #*LRRK2 Mutation
        self.LRRK2_Mutation = tk.Label(self.frame_in_canvas_Inputs, text="LRRK2")
        self.LRRK2_Mutation.grid(row=7, column=0)
        self.LRRK2_var = tk.IntVar()
        self.LRRK2_Mutation_checkbox = tk.Checkbutton(self.frame_in_canvas_Inputs, variable=self.LRRK2_var)
        self.LRRK2_Mutation_checkbox.grid(row=7, column=1)
        
        #*GBA1 Mutation
        self.GBA1_Mutation = tk.Label(self.frame_in_canvas_Inputs, text="GBA1")
        self.GBA1_Mutation.grid(row=8, column=0)
        self.GBA1_var = tk.IntVar()
        self.GBA1_Mutation_checkbox = tk.Checkbutton(self.frame_in_canvas_Inputs, variable=self.GBA1_var)
        self.GBA1_Mutation_checkbox.grid(row=8, column=1)        
        
        #*VPS35 Mutation
        self.VPS35_Mutation = tk.Label(self.frame_in_canvas_Inputs, text="VPS35")
        self.VPS35_Mutation.grid(row=9, column=0)
        self.VPS35_var = tk.IntVar()
        self.VPS35_Mutation_checkbox = tk.Checkbutton(self.frame_in_canvas_Inputs, variable=self.VPS35_var)
        self.VPS35_Mutation_checkbox.grid(row=9, column=1)          

        #*DJ1 Mutation
        self.DJ1_Mutation = tk.Label(self.frame_in_canvas_Inputs, text="DJ1")
        self.DJ1_Mutation.grid(row=10, column=0)
        self.DJ1_var = tk.IntVar()
        self.DJ1_Mutation_checkbox = tk.Checkbutton(self.frame_in_canvas_Inputs, variable=self.DJ1_var)
        self.DJ1_Mutation_checkbox.grid(row=10, column=1)   
        
        #*Therapeutics Header*
        self.Therapeutics_Header = tkfont.Font(family='Helvetica', size=10, weight="bold", slant="italic") 
        self.Label_Header_Therapeutics = tk.Label(self.frame_in_canvas_Inputs, text="Therapeutics", font=self.Therapeutics_Header)
        self.Label_Header_Therapeutics.grid(row=11, column=1)
        
        #NPT200
        self.PD_NPT200 = tk.Label(self.frame_in_canvas_Inputs, text="NPT200")
        self.PD_NPT200.grid(row=12, column=0)
        self.PD_NPT200_var = tk.IntVar()
        self.PD_NPT200_checkbox = tk.Checkbutton(self.frame_in_canvas_Inputs, variable=self.PD_NPT200_var)
        self.PD_NPT200_checkbox.grid(row=12, column=1) 
        
        #DNL151
        self.PD_DNL151 = tk.Label(self.frame_in_canvas_Inputs, text="DNL151")
        self.PD_DNL151.grid(row=13, column=0)
        self.PD_DNL151_var = tk.IntVar()
        self.PD_DNL151_checkbox = tk.Checkbutton(self.frame_in_canvas_Inputs, variable=self.PD_DNL151_var)
        self.PD_DNL151_checkbox.grid(row=13, column=1)        
    
        #LAMP2A
        self.PD_LAMP2A = tk.Label(self.frame_in_canvas_Inputs, text="LAMP2A")
        self.PD_LAMP2A.grid(row=14, column=0)
        self.PD_LAMP2A_var = tk.IntVar()
        self.PD_LAMP2A_checkbox = tk.Checkbutton(self.frame_in_canvas_Inputs, variable=self.PD_LAMP2A_var)
        self.PD_LAMP2A_checkbox.grid(row=14, column=1)  
        
        def save_entry_inputs(self):
            self.HFPN_run_save_name =self.Label_run_save_name_e.get()
            self.HFPN_number_of_timesteps = self.Label_no_timesteps_e.get()
            self.HFPN_timestep_size = self.Label_timestep_size_e.get()
            self.HFPN_CholSD = self.Label_CholSD_e.get()
            self.HFPN_CalciumSD = self.Label_Calcium_e.get()
            print("Inputs Saved")
            self.button_1.config(state="normal", text="Run sHFPN")
            self.AD_button_1.config(state="normal", text="Run AD sHFPN")            
            self.button_6.config(state=tk.DISABLED)
            
        #*Save Inputs Button*
        self.button_6 = tk.Button(self.frame_in_canvas_Inputs, text = "Save Inputs", cursor="hand2", command=partial(save_entry_inputs, self))    
        self.button_6.grid(row=20, column=1, pady=20)  
        self.Label_Save_Inputs_Button_info = tk.Label(self.frame_in_canvas_Inputs, text="Double check your inputs")
        self.Label_Save_Inputs_Button_info.grid(row=20, column=2)
            
    def About_Page(self):
        self.frame7=tk.Frame(self.frame2)
        self.frame7.grid(row=0, column=0, sticky="nsew")
        self.button_4 = tk.Button(self.frame7, text="Link to Website")
        def Open_Link(url):
            webbrowser.open_new(url)
        self.button_4.config(cursor="hand2",command= partial(Open_Link, "https://www.ceb-mng.org/"))
        self.button_4.pack()
        self.button_5 = tk.Button(self.frame7, text="Twitter", cursor="hand2", command = partial(Open_Link, "https://twitter.com/mng_ceb"))
        self.button_5.pack(side="top")

        self.About_Image = ImageTk.PhotoImage(Image.open("AboutPage.png"))
        self.Image_as_Label = tk.Label(self.frame7)
        self.Image_as_Label.config(image=self.About_Image)
        self.Image_as_Label.pack()
        self.BSL_font = tkfont.Font(family='Helvetica', size=7, slant="italic")
        self.Label_BSL = tk.Label(self.frame7, text="Please email B.S. Lockey at bsl29@cam.ac.uk for issues.", font=self.BSL_font)
        self.Label_BSL.pack()

    def Neuronal_HealthBar(self):
        self.frame8=tk.Frame(self.frame2)
        self.frame8.grid(row=0, column=0, sticky="nsew")
        
        #Label
        self.Label_Neuronal_Healthbar = tk.Label(self.frame8, text="Under Construction...")
        self.Label_Neuronal_Healthbar.pack()
        
        #Embedded Graphs (PROBABLY HAVE TO APPEND THIS TO SELF LATER, SO CAN BE ACCESSED)
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8],[1,2,3,4,5,6,7,8])
        Neuronal_Healthbar_canvas = FigureCanvasTkAgg(f, self.frame8)
        Neuronal_Healthbar_canvas.draw()
        Neuronal_Healthbar_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)#I can also choose to grid it so its more compact for later, when I want to plot multiple plots. 
        toolbar = NavigationToolbar2Tk(Neuronal_Healthbar_canvas, self.frame8)
        toolbar.update()
        Neuronal_Healthbar_canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def Run_AD_sHFPN_Page(self):
        self.AD_frame1=tk.Frame(self.frame2)
        #self.frame4.pack(side="left", fill=tk.BOTH,expand=1)
        self.AD_frame1.grid(row=0,column=0,sticky="nsew")
        self.AD_button_1 = tk.Button(self.AD_frame1, text="Please Save Inputs", state=tk.DISABLED, command= threading.Thread(target = partial(self.run_AD_sHFPN)).start)
        self.AD_button_1.config(cursor="hand2")
        self.AD_button_1.pack(side=tk.TOP)
        self.make_scrollbar_AD_sHFPN()        
        
        
    def Run_sHFPN_Page(self):
        self.frame4=tk.Frame(self.frame2)
        #self.frame4.pack(side="left", fill=tk.BOTH,expand=1)
        self.frame4.grid(row=0,column=0,sticky="nsew")
        self.button_1 = tk.Button(self.frame4, text="Please Save Inputs", state=tk.DISABLED, command= threading.Thread(target = partial(self.run_sHFPN)).start)
        self.button_1.config(cursor="hand2")
        self.button_1.pack(side=tk.TOP)
        self.make_scrollbar_sHFPN()
        
    def Analysis_page(self):
        self.frame5=tk.Frame(self.frame2)
        #self.frame5.pack(side="left", fill=tk.BOTH,expand=1)
        self.frame5.grid(row=0,column=0,sticky="nsew")
        self.run_save_name_entry = tk.Entry(self.frame5, width=50, bg="black", fg="violet", borderwidth="5")
        self.run_save_name_entry.pack()
        
        def save_entry(self):
            "saves run_save_name entry"
            self.run_save_name =self.run_save_name_entry.get()
            self.button_2.config(state="normal", text="Run Analysis")
            print(self.run_save_name)
            self.button3.config(state=tk.DISABLED)
            
        self.button3 = tk.Button(self.frame5, text="Enter run_save_name", command = partial(save_entry, self))
        self.button3.config(cursor="hand2")
        self.button3.pack()
        

            
        
        def GUI_plot(place_id, analysis, File):
            token_storage = analysis[File].token_storage        
            place_label =""
            plot_title = place_id
            t=np.arange(0,(desired_plotting_steps/(1/simulation_time_step))+simulation_time_step,simulation_time_step) #
          
            fig,ax=plt.subplots()
            linestep = 0.3
            line_width = 2.5
            
            data = analysis[File].mean_token_history_for_places([place_id])[0:desired_plotting_steps+1] 
            #print(data[1600000]) #units in time_step
            #print(data[1800000])
            if place_label == "":
                ax.plot(t, data, label = File,  color="black")
            else:
                ax.plot(t, data, label = File+' - '+place_label, color="black")
            
            ax.legend()
            Analysis.standardise_plot(ax, title = plot_title, xlabel = "Time (s)",ylabel = "Molecule count")
            plt.show()
            
        def run_Analysis(self):
            self.button_2.config(text="Please Wait, Loading...", state=tk.DISABLED)
            run_save_name = self.run_save_name
            analysis = {}
            start_time = datetime.now()
            
            #File1 = '200k_sHFPN_Healthy_SD_01_DelaySD_01_run3_V3_TRANSITION'
            #File2 = '6e6_sHFPN_Healthy_SD_0_DelaySD_02'
            File3 = run_save_name
            global desired_plotting_steps
            desired_plotting_steps = number_time_steps
            global simulation_time_step
            simulation_time_step = time_step_size
            
            #analysis[File1] = Analysis.load_from_file(File1)
            #analysis[File2] = Analysis.load_from_file(File2)
            analysis[File3] = Analysis.load_from_file(File3)
            
            execution_time = datetime.now()-start_time
            print('\n\nLoad-in Time:', execution_time)
            print("")    
            
            list_of_place_names = []
            for place in analysis[File3].place_ids:
                list_of_place_names.append(place)
            
            tk.Button(self.frame_in_canvas_Analysis, text = "Places").grid(row=0, column=0, pady=10, padx=10)
            
            for index, place_id in enumerate(list_of_place_names):
                tk.Button(self.frame_in_canvas_Analysis, text=place_id, command=partial(GUI_plot, place_id, analysis, File3)).grid(row=index+1, column=0, pady=10, padx=10)#pass value as an argument to plot  
            self.button_2.config(text="Restart Session to Run Another Analysis", state=tk.DISABLED)
           

        self.button_2 = tk.Button(self.frame5, text="Please Enter Save Name", state=tk.DISABLED, command= threading.Thread(target = partial(run_Analysis,self)).start)
        self.button_2.config(cursor="hand2")
        self.button_2.pack(side=tk.TOP)
        self.make_scrollbar_Analysis()
    
    def show_saved_runs(self):
        self.frame6=tk.Frame(self.frame2)
        #self.frame6.pack(side="left", fill=tk.BOTH,expand=1)  
        self.frame6.grid(row=0,column=0,sticky="nsew")
        self.lbx = tk.Listbox(self.frame6)
        self.lbx.pack(fill=tk.BOTH, expand=1)
        
        if platform == 'darwin':
            for file in glob.glob("../saved-runs/*"):
                self.lbx.insert(tk.END, file)  
        if platform == 'win32':
            for file in glob.glob("..\saved-runs\*"):
                self.lbx.insert(tk.END, file) 
                
    def hide(self):
        if self.hidden == 0:
            self.frame1.destroy()
            self.hidden=1
        elif self.hidden==1:
            self.frame2.destroy()
            self.hidden=0
            self.Left_Sidebar()
            self.Right_Output()
                
   

    def run_sHFPN(self):
        
        #Save Inputs from GUI
        run_save_name = self.HFPN_run_save_name
        number_time_steps = int(self.HFPN_number_of_timesteps)
        time_step_size = float(self.HFPN_timestep_size)
        cholSD = float(self.HFPN_CholSD)
        DelaySD = float(self.HFPN_CalciumSD)     
        #*Get all Mutations*
        it_p_LRRK2_mut = self.LRRK2_var.get()
        it_p_GBA1 = self.GBA1_var.get()
        it_p_VPS35 = self.VPS35_var.get()
        it_p_DJ1 = self.DJ1_var.get()
        
        #*Therapeutics*
        it_p_NPT200 = self.PD_NPT200_var.get()
        it_p_DNL151 = self.PD_DNL151_var.get()
        it_p_LAMP2A = self.PD_LAMP2A_var.get()
        
        #Disable Run HFPN Button
        self.button_1.config(state=tk.DISABLED)
        self.button_1.config(text="Running Simulation... Please bear with Lag...")
        # Initialize an empty HFPN
        pn = HFPN(time_step = time_step_size) #unit = s/A.U.    
        
        ## Define places
    
       #  # Cholesterol homeostasis
        pn.add_place(it_p_chol_PM, "p_chol_PM","Chol - perinuclear region", continuous = True)
        pn.add_place(it_p_chol_LE, "p_chol_LE", "Chol - late endosome", continuous = True)
        pn.add_place(it_p_chol_ER, "p_chol_ER", "Chol - ER", continuous = True)
        pn.add_place(it_p_chol_mito, "p_chol_mito", "Chol - mitochondria", continuous = True)
        pn.add_place(it_p_27OHchol_extra, "p_27OHchol_extra","27-OH chol - extracellular", continuous = True)
        pn.add_place(it_p_27OHchol_intra, "p_27OHchol_intra","27-OH chol - intracellular", continuous = True)
        pn.add_place(it_p_ApoEchol_extra, "p_ApoEchol_extra","ApoE - extracellular", continuous = True)
        pn.add_place(it_p_ApoEchol_EE, "p_ApoEchol_EE","ApoE - Early endosome", continuous = True)
        pn.add_place(it_p_7HOCA, "p_7HOCA","7-HOCA", continuous = True)
        pn.add_place(it_p_preg,place_id="p_preg", label="Pregnenolon", continuous=True)
        pn.add_place(it_p_24OHchol_extra,place_id="p_24OHchol_extra", label="24OHchol extra", continuous=True)
        pn.add_place(it_p_24OHchol_intra,place_id="p_24OHchol_intra", label="24OHchol intra", continuous=True)
    
        #  # PD specific places in cholesterol homeostasis
        pn.add_place(it_p_GBA1, "p_GBA1","GBA1", continuous = False)
        pn.add_place(it_p_SNCA_act_extra, "p_SNCA_act_extra","a-synuclein - extracellular", continuous = True)
        pn.add_place(it_p_SNCAApoEchol_extra, "p_SNCAApoEchol_extra","a-synuclein-ApoE complex - extracellular", continuous = True)
        pn.add_place(it_p_SNCAApoEchol_intra, "p_SNCAApoEchol_intra","a-synuclein-ApoE complex - intracellular", continuous = True)
    
        #  # Energy metabolism
        pn.add_place(it_p_ROS_mito, "p_ROS_mito", "ROS - mitochondria", continuous = True)
        pn.add_place(it_p_H2O_mito, "p_H2O_mito", "H2O - mitochondria", continuous = True)
        pn.add_place(it_p_reduc_mito, "p_reduc_mito", "Reducing agents - mitochondria", continuous = True)
        pn.add_place(it_p_cas3, "p_cas3","caspase 3 - mitochondria", continuous = True)
        pn.add_place(it_p_DJ1, "p_DJ1","DJ1 mutant", continuous = True)
        
        #  # Calcium homeostasis
        pn.add_place(it_p_Ca_cyto, "p_Ca_cyto", "Ca - cytosole", continuous = True)
        pn.add_place(it_p_Ca_mito, "p_Ca_mito","Ca - mitochondria", continuous = True)
        pn.add_place(it_p_Ca_ER, "p_Ca_ER", "Ca - ER", continuous = True)
        pn.add_place(it_p_ADP, "p_ADP","ADP - Calcium ER import", continuous = True)
        pn.add_place(it_p_ATP, "p_ATP","ATP - Calcium ER import", continuous = True)
    
        #  # Discrete on/of-switches calcium pacemaking
    
        pn.add_place(1, "p_Ca_extra", "on1 - Ca - extracellular", continuous = False)
        pn.add_place(0, "p_on2","on2", continuous = False)
        pn.add_place(0, "p_on3","on3", continuous = False)
        pn.add_place(0, "p_on4","on4", continuous = False)
        
          # Lewy bodies
        pn.add_place(it_p_SNCA_act, "p_SNCA_act","SNCA - active", continuous = True)
        pn.add_place(it_p_VPS35, "p_VPS35", "VPS35", continuous = True)
        pn.add_place(it_p_SNCA_inact, "p_SNCA_inact", "SNCA - inactive", continuous = True)
        pn.add_place(it_p_SNCA_olig, "p_SNCA_olig", "SNCA - Oligomerised", continuous = True)
        pn.add_place(it_p_LB, "p_LB", "Lewy body", continuous = True)
        pn.add_place(it_p_Fe2, "p_Fe2", "Fe2 iron pool", continuous = True)
        
          # Late endosome pathology 
        pn.add_place(it_p_LRRK2_mut, "p_LRRK2_mut","LRRK2 - mutated", continuous = True)
          # Monomeric RTN3 (cycling between axonal and perinuclear regions)
        pn.add_place(it_p_RTN3_axon, place_id="p_RTN3_axon", label="monomeric RTN3 (axonal)", continuous=True)
        pn.add_place(it_p_RTN3_PN, place_id="p_RTN3_PN", label="monomeric RTN3 (perinuclear)", continuous=True)
    
          # HMW RTN3 (cycling between different cellular compartments)
        pn.add_place(it_p_RTN3_HMW_cyto, place_id="p_RTN3_HMW_cyto", label="HMW RTN3 (cytosol)", continuous=True)
        pn.add_place(it_p_RTN3_HMW_auto, place_id="p_RTN3_HMW_auto", label="HMW RTN3 (autophagosome)", continuous=True)
        pn.add_place(it_p_RTN3_HMW_lyso, place_id="p_RTN3_HMW_lyso", label="HMW RTN3 (degraded in lysosome)", continuous=True)
        pn.add_place(it_p_RTN3_HMW_dys1, place_id="p_RTN3_HMW_dys1", label="HMW RTN3 (type I/III dystrophic neurites)", continuous=True)
        pn.add_place(it_p_RTN3_HMW_dys2, place_id="p_RTN3_HMW_dys2", label="HMW RTN3 (type II dystrophic neurites)", continuous=True)
    
          # Two places that are NOT part of this subpathway, but are temporarily added for establishing proper connections
          # They will be removed upon merging of subpathways
        pn.add_place(it_p_tau, place_id="p_tau", label = "Unphosphorylated tau", continuous = True)
        pn.add_place(it_p_tauP, place_id="p_tauP", label = "Phosphorylated tau", continuous = True)
        
        # Drug places 
        pn.add_place(it_p_NPT200, place_id="p_NPT200", label = "Drug NPT200", continuous = True)
        pn.add_place(it_p_DNL151, place_id="p_DNL151", label = "Drug DNL151", continuous = True)
        pn.add_place(it_p_LAMP2A, place_id="p_LAMP2A", label = "Drug LAMP2A", continuous = True)
        
        ## Define transitions
        
        # Cholesterol Endocytosis
        pn.add_transition_with_speed_function( #1
                        transition_id                 = "t_LDLR_endocyto",
                        label                          = "LDLR endocyto",
                        input_place_ids                 = ["p_ApoEchol_extra", "p_chol_ER","p_LB"],
                        firing_condition             = fc_t_LDLR_endocyto,
                        reaction_speed_function         = r_t_LDLR_endocyto, 
                        consumption_coefficients     = [0,0,0],
                        output_place_ids             = ["p_ApoEchol_EE"],
                        production_coefficients         = [1],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # # Cleavage of cholesteryl esters
        pn.add_transition_with_speed_function( #2
                        transition_id                 = "t_ApoEchol_cleav",
                        label                          = "ApoE-chol cleav",
                        input_place_ids                 = ["p_ApoEchol_EE"],
                        firing_condition             = fc_t_ApoEchol_cleav,
                        reaction_speed_function         = r_t_ApoEchol_cleav, 
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_chol_LE"],
                        production_coefficients         = [354],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # Transport Cholesterol from LE to ER
        pn.add_transition_with_speed_function( #3
                        transition_id                 = "t_chol_trans_LE_ER",
                        label                          = "Chol transport LE-ER",
                        input_place_ids                 = ["p_chol_LE"],
                        firing_condition             = fc_t_chol_trans_LE_ER,
                        reaction_speed_function         = r_t_chol_trans_LE_ER,
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_chol_ER"],
                        production_coefficients         = [1],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # Transport Cholesterol from LE to mito
        pn.add_transition_with_speed_function( #4
                        transition_id                 = "t_chol_trans_LE_mito",
                        label                          = "Chol transport LE-mito",
                        input_place_ids                 = ["p_chol_LE"],
                        firing_condition             = fc_t_chol_trans_LE_mito,
                        reaction_speed_function         = r_t_chol_trans_LE_mito,
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_chol_mito"],
                        production_coefficients         = [1],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # Transport Cholesterol from LE to PM
        pn.add_transition_with_speed_function( #5
                        transition_id                 = "t_chol_trans_LE_PM",
                        label                          = "Chol transport LE-PM",
                        input_place_ids                 = ["p_chol_LE"],
                        firing_condition             = fc_t_chol_trans_LE_PM, 
                        reaction_speed_function         = r_t_chol_trans_LE_PM,
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_chol_PM"],
                        production_coefficients         = [1],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # Transport Cholesterol from PM to ER
        pn.add_transition_with_speed_function( #6
                        transition_id                 = "t_chol_trans_PM_ER",
                        label                          = "Chol transport PM-ER",
                        input_place_ids                 = ["p_chol_PM"],
                        firing_condition             = fc_t_chol_trans_PM_ER,
                        reaction_speed_function         = r_t_chol_trans_PM_ER,
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_chol_ER"],
                        production_coefficients         = [1],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # Transport Cholesterol from ER to PM
        pn.add_transition_with_speed_function( #7
                        transition_id                 = "t_chol_trans_ER_PM",
                        label                          = "Chol transport ER-PM",
                        input_place_ids                 = ["p_chol_ER"],
                        firing_condition             = fc_t_chol_trans_ER_PM,
                        reaction_speed_function         = r_t_chol_trans_ER_PM,
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_chol_PM"],
                        production_coefficients         = [1],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # Transport Cholesterol from ER to mito
        pn.add_transition_with_speed_function( #8
                        transition_id                 = "t_chol_trans_ER_mito",
                        label                          = "Chol transport ER-mito",
                        input_place_ids                 = ["p_chol_ER"],
                        firing_condition             = fc_t_chol_trans_ER_mito,
                        reaction_speed_function         = r_t_chol_trans_ER_mito,
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_chol_mito"],
                        production_coefficients         = [1],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # Metabolisation of chol by CYP27A1
        pn.add_transition_with_michaelis_menten( #9
                        transition_id                 = "t_CYP27A1_metab",
                        label                          = "Chol metab CYP27A1",
                        Km                             = Km_t_CYP27A1_metab,
                        vmax                         = vmax_t_CYP27A1_metab,
                        input_place_ids                 = ["p_chol_mito"],
                        substrate_id                 = "p_chol_mito",
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_27OHchol_intra"],
                        production_coefficients         = [1],
                        vmax_scaling_function         = lambda a : chol_mp,
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # Metabolism of chol by CYP11A1
        pn.add_transition_with_michaelis_menten( #10
                        transition_id                 = "t_CYP11A1_metab",
                        label                          = "Chol metab CYP11A1",
                        Km                             = Km_t_CYP11A1_metab,
                        vmax                         = vmax_t_CYP11A1_metab,
                        input_place_ids                 = ["p_chol_mito"],
                        substrate_id                 = "p_chol_mito",
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_preg"],
                        production_coefficients         = [1],
                        vmax_scaling_function         = lambda a : chol_mp,
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # Metabolisation of 27OHchol by CYP7B1
        pn.add_transition_with_michaelis_menten( #11
                        transition_id                 = "t_CYP7B1_metab",
                        label                          = "27OHchol metab CYP7B1",
                        Km                             = Km_t_CYP7B1_metab,
                        vmax                         = vmax_t_CYP7B1_metab,
                        input_place_ids                 = ["p_27OHchol_intra"],
                        substrate_id                 = "p_27OHchol_intra",
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_7HOCA"],
                        production_coefficients         = [1],
                        vmax_scaling_function         = lambda a : chol_mp,
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # Endocytosis of 27OHchol
        pn.add_transition_with_speed_function( #12
                        transition_id                 = "t_27OHchol_endocyto",
                        label                          = "27OHchol endocyto",
                        input_place_ids                 = ["p_27OHchol_extra"],
                        firing_condition             = fc_t_27OHchol_endocyto,
                        reaction_speed_function         = r_t_27OHchol_endocyto,
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_27OHchol_intra", "p_27OHchol_extra"],
                        production_coefficients         = [1,1],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # Metabolisation of chol by CYP46A1
        pn.add_transition_with_michaelis_menten( #13
                        transition_id                 = "t_CYP46A1_metab",
                        label                          = "Chol metab CYP46A1",
                        Km                             = Km_t_CYP46A1_metab,
                        vmax                         = vmax_t_CYP46A1_metab,
                        input_place_ids                 = ["p_chol_ER"],
                        substrate_id                 = "p_chol_ER",
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_24OHchol_intra"],
                        production_coefficients         = [1],
                        vmax_scaling_function         = lambda a : chol_mp,
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # Exocytosis of 24OHchol
        pn.add_transition_with_speed_function( #14
                        transition_id                 = "t_24OHchol_exocyto",
                        label                          = "24OHchol exocyto",
                        input_place_ids                 = ["p_24OHchol_intra"],
                        firing_condition             = fc_t_24OHchol_exocyto,
                        reaction_speed_function         = r_t_24OHchol_exocyto,
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_24OHchol_extra"],
                        production_coefficients         = [1],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # Transport of Chol into ECM
        pn.add_transition_with_speed_function( #15
                        transition_id                 = "t_chol_trans_PM_ECM",
                        label                          = "Chol transport PM-ECM",
                        input_place_ids                 = ["p_chol_PM", "p_24OHchol_intra"],
                        firing_condition             = fc_t_chol_trans_PM_ECM,
                        reaction_speed_function         = r_t_chol_trans_PM_ECM,
                        consumption_coefficients     = [1,0],
                        output_place_ids             = [],
                        production_coefficients         = [],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = ["yes", "no"])
    
    
        # PD specific
    
        pn.add_transition_with_speed_function( #16
                            transition_id = 't_SNCA_bind_ApoEchol_extra',
                            label = 'Extracellular binding of SNCA to chol',
                            input_place_ids = ['p_ApoEchol_extra','p_SNCA_act'],
                            firing_condition = fc_t_SNCA_bind_ApoEchol_extra,
                            reaction_speed_function = r_t_SNCA_bind_ApoEchol_extra,
                            consumption_coefficients = [0,30], 
                            output_place_ids = ['p_SNCA_olig'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
    
        pn.add_transition_with_speed_function( #17
                            transition_id = 't_chol_LE_upreg',
                            label = 'Upregulation of chol in LE',
                            input_place_ids = ['p_GBA1'],
                            firing_condition = fc_t_chol_LE_upreg,
                            reaction_speed_function = r_t_chol_LE_upreg,
                            consumption_coefficients = [0], # GBA1 is an enzyme
                            output_place_ids = ['p_chol_LE'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
        
        # # Calcium homeostasis
        
        pn.add_transition_with_speed_function( #18
                            transition_id = 't_Ca_imp',
                            label = 'L-type Ca channel',
                            input_place_ids = ['p_Ca_extra'],
                            firing_condition = fc_t_Ca_imp,
                            reaction_speed_function = r_t_Ca_imp,
                            consumption_coefficients = [0], # Need to review this 
                            output_place_ids = ['p_Ca_cyto'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) # Need to review this 
    
    
        pn.add_transition_with_speed_function( #19
                            transition_id = 't_mCU',
                            label = 'Ca import into mitochondria via mCU',
                            input_place_ids = ['p_Ca_cyto','p_Ca_mito'],
                            firing_condition = fc_t_mCU,
                            reaction_speed_function = r_t_mCU,
                            consumption_coefficients = [1,0], 
                            output_place_ids = ['p_Ca_mito'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect)
    
        pn.add_transition_with_speed_function( #20
                            transition_id = 't_MAM',
                            label = 'Ca transport from ER to mitochondria',
                            input_place_ids = ['p_Ca_ER','p_Ca_mito'],
                            firing_condition = fc_t_MAM,
                            reaction_speed_function = r_t_MAM,
                            consumption_coefficients = [1,0], 
                            output_place_ids = ['p_Ca_mito'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect)
    
        pn.add_transition_with_speed_function( #21
                            transition_id = 't_RyR_IP3R',
                            label = 'Ca export from ER',
                            input_place_ids = ['p_Ca_extra','p_Ca_ER'],
                            firing_condition = fc_t_RyR_IP3R,
                            reaction_speed_function = r_t_RyR_IP3R,
                            consumption_coefficients = [0,1], 
                            output_place_ids = ['p_Ca_cyto'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) 
    
        pn.add_transition_with_speed_function( #22
                            transition_id = 't_SERCA',
                            label = 'Ca import to ER',
                            input_place_ids = ['p_Ca_cyto','p_ATP'],
                            firing_condition = fc_t_SERCA,
                            reaction_speed_function = r_t_SERCA,
                            consumption_coefficients = [1,1], #!!!!! Need to review this 0 should be 1
                            output_place_ids = ['p_Ca_ER','p_ADP'],         
                            production_coefficients = [1,1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) # Need to review this
    
        pn.add_transition_with_speed_function( #23
                            transition_id = 't_NCX_PMCA',
                            label = 'Ca efflux to extracellular space',
                            input_place_ids = ['p_Ca_cyto','p_on3'],
                            firing_condition = lambda a: a['p_on3']==1,
                            reaction_speed_function = r_t_NCX_PMCA,
                            consumption_coefficients = [1,0], 
                            output_place_ids = [],         
                            production_coefficients = [],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect)
        
        pn.add_transition_with_speed_function( #24
                            transition_id = 't_mNCLX',
                            label = 'Ca export from mitochondria via mNCLX',
                            input_place_ids = ['p_Ca_mito','p_LRRK2_mut'],
                            firing_condition = fc_t_mNCLX,
                            reaction_speed_function = r_t_mNCLX,
                            consumption_coefficients = [1,0], 
                            output_place_ids = ['p_Ca_cyto'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) 
    
        # # Discrete on/off-switches calcium pacemaking
    
        pn.add_transition_with_speed_function( #25
                            transition_id = 't_A',
                            label = 'A',
                            input_place_ids = ['p_on4'],
                            firing_condition = lambda a: a['p_on4']==1,
                            reaction_speed_function = lambda a: 1,
                            consumption_coefficients = [1], 
                            output_place_ids = ['p_Ca_extra'],         
                            production_coefficients = [1],
                            stochastic_parameters = [CaSD,DelaySD],
                            collect_rate_analytics = ["no","no"],
                            delay=0.5) 
        
        pn.add_transition_with_speed_function( #26
                            transition_id = 't_B',
                            label = 'B',
                            input_place_ids = ['p_Ca_extra'],
                            firing_condition = lambda a: a['p_Ca_extra']==1,
                            reaction_speed_function = lambda a: 1,
                            consumption_coefficients = [1], 
                            output_place_ids = ['p_on2'],         
                            production_coefficients = [1],
                            stochastic_parameters = [CaSD,DelaySD],
                            collect_rate_analytics = ["no","no"],
                            delay=0.5) 
        pn.add_transition_with_speed_function( #27
                            transition_id = 't_C',
                            label = 'C',
                            input_place_ids = ['p_on2'],
                            firing_condition = lambda a: a['p_on2']==1,
                            reaction_speed_function = lambda a: 1,
                            consumption_coefficients = [1], 
                            output_place_ids = ['p_on3'],         
                            production_coefficients = [1],
                            stochastic_parameters = [CaSD,0],
                            collect_rate_analytics = ["no","no"],
                            delay=0) 
        pn.add_transition_with_speed_function( #28
                            transition_id = 't_D',
                            label = 'D',
                            input_place_ids = ['p_on3'],
                            firing_condition = lambda a: a['p_on3']==1,
                            reaction_speed_function = lambda a: 1,
                            consumption_coefficients = [1], 
                            output_place_ids = ['p_on4'],         
                            production_coefficients = [1],
                            stochastic_parameters = [CaSD,DelaySD],
                            collect_rate_analytics = ["no","no"],
                            delay=0.5)
        
        # Link to energy metabolism in that it needs ATP replenishment
        pn.add_transition_with_mass_action( #29
                            transition_id = 't_NaK_ATPase',
                            label = 'NaK ATPase',
                            rate_constant =  k_t_NaK_ATPase,
                            input_place_ids = ['p_ATP', 'p_on3'],
                            firing_condition = lambda a: a['p_on3']==1,
                            consumption_coefficients = [1,0], 
                            output_place_ids = ['p_ADP'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) 
        
       # Lewy bodies pathology
        pn.add_transition_with_speed_function( #30
                            transition_id = 't_SNCA_degr',
                            label = 'SNCA degradation by CMA',
                            input_place_ids = ['p_SNCA_act','p_VPS35','p_LRRK2_mut','p_27OHchol_intra','p_DJ1', 'p_DNL151', 'p_LAMP2A'],
                            firing_condition = fc_t_SNCA_degr,
                            reaction_speed_function = r_t_SNCA_degr,
                            consumption_coefficients = [1,0,0,0,0,0,0], 
                            output_place_ids = ['p_SNCA_inact'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics) 
    
        pn.add_transition_with_speed_function(#31
                            transition_id = 't_SNCA_aggr',
                            label = 'SNCA aggregation',
                            input_place_ids = ['p_SNCA_act','p_Ca_cyto','p_ROS_mito', 'p_tauP', 'p_NPT200'],
                            firing_condition = fc_t_SNCA_aggr,
                            reaction_speed_function = r_t_SNCA_aggr,
                            consumption_coefficients = [30,0,0,0,0], #should be reviewed if Ca is consumed
                            output_place_ids = ['p_SNCA_olig'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics) 
    
        pn.add_transition_with_speed_function(#32
                            transition_id = 't_SNCA_fibril',
                            label = 'SNCA fibrillation',
                            input_place_ids = ['p_SNCA_olig'],
                            firing_condition = fc_t_SNCA_fibril,
                            reaction_speed_function = r_t_SNCA_fibril,
                            consumption_coefficients = [100], 
                            output_place_ids = ['p_LB'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics) 
    
        pn.add_transition_with_speed_function(#33
                            transition_id = 't_IRE',
                            label = 'IRE',
                            input_place_ids = ['p_Fe2'],
                            firing_condition = fc_t_IRE,
                            reaction_speed_function = r_t_IRE,
                            consumption_coefficients = [0], 
                            output_place_ids = ['p_SNCA_act'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics) 
        
        # Energy metabolism
        pn.add_transition_with_speed_function(#34
                            transition_id = 't_ATP_hydro_mito',
                            label = 'ATP hydrolysis in mitochondria',
                            input_place_ids = ['p_ATP'],
                            firing_condition = fc_t_ATP_hydro_mito,
                            reaction_speed_function = r_t_ATP_hydro_mito,
                            consumption_coefficients = [1], 
                            output_place_ids = ['p_ADP'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) 
        
        pn.add_transition_with_speed_function(#35
                            transition_id = 't_ROS_metab',
                            label = 'ROS neutralisation',
                            input_place_ids = ['p_ROS_mito','p_chol_mito','p_LB','p_DJ1'],
                            firing_condition = fc_t_ROS_metab,
                            reaction_speed_function = r_t_ROS_metab,
                            consumption_coefficients = [1,0,0,0], 
                            output_place_ids = ['p_H2O_mito'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics) 
        # #Link of krebs to calcium homeostasis
        pn.add_transition_with_speed_function(#36
                            transition_id = 't_krebs',
                            label = 'Krebs cycle',
                            input_place_ids = ['p_ADP','p_Ca_mito'],
                            firing_condition = fc_t_krebs,
                            reaction_speed_function = r_t_krebs,
                            consumption_coefficients = [1,0], # Need to review this
                            output_place_ids = ['p_reduc_mito','p_ATP'],         
                            production_coefficients = [4,1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics) 
        
        #Link of ETC to calcium and cholesterol
        pn.add_transition_with_speed_function(#37
                            transition_id = 't_ETC',
                            label = 'Electron transport chain',
                            input_place_ids = ['p_reduc_mito', 'p_ADP', 'p_Ca_mito', 'p_chol_mito','p_ROS_mito','p_LRRK2_mut'],
                            firing_condition = fc_t_ETC,
                            reaction_speed_function = r_t_ETC,
                            consumption_coefficients = [22/3,22,0,0,0,0], # Need to review this
                            output_place_ids = ['p_ATP', 'p_ROS_mito'],         
                            production_coefficients = [22,0.005],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics) 
    
        # # Output transitions: Cas3 for apoptosis
        pn.add_transition_with_speed_function(#38
                            transition_id = 't_mito_dysfunc',
                            label = 'Mitochondrial complex 1 dysfunction',
                            input_place_ids = ['p_ROS_mito'],
                            firing_condition = fc_t_mito_dysfunc,
                            reaction_speed_function = r_t_mito_dysfunc,
                            consumption_coefficients = [1], 
                            output_place_ids = ['p_cas3'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics) 
        
        pn.add_transition_with_speed_function(#39
                            transition_id = 't_cas3_inact',
                            label = 'Caspase 3 degredation',
                            input_place_ids = ['p_cas3'],
                            firing_condition = fc_t_cas3_inact,
                            reaction_speed_function = r_t_cas3_inact,
                            consumption_coefficients = [1], # Need to review this
                            output_place_ids = [],         
                            production_coefficients = [],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) 
        
        # Late endosome pathology
        pn.add_transition_with_michaelis_menten(#40
                            transition_id = 't_phos_tau',
                            label = 'Phosphorylation of tau',
                            Km = Km_t_phos_tau, 
                            vmax = kcat_t_phos_tau, 
                            input_place_ids = ['p_tau', 'p_SNCA_act'],
                            substrate_id = 'p_tau',
                            consumption_coefficients = [1, 0],
                            output_place_ids = ['p_tauP'],
                            production_coefficients = [1],
                            vmax_scaling_function = vmax_scaling_t_phos_tau,
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) 
    
        pn.add_transition_with_michaelis_menten(#41
                            transition_id = 't_dephos_tauP',
                            label = 'Dephosphorylation of tau protein',
                            Km = Km_t_dephos_tauP, 
                            vmax = vmax_t_dephos_tauP, 
                            input_place_ids = ['p_tauP', 'p_Ca_cyto'],
                            substrate_id = 'p_tauP',
                            consumption_coefficients = [1, 0],
                            output_place_ids = ['p_tau'],
                            production_coefficients = [1],
                            vmax_scaling_function = vmax_scaling_t_dephos_tauP,
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) 
    
        pn.add_transition_with_speed_function(#42
                            transition_id = 't_RTN3_exp',
                            label = 'Expression rate of RTN3',
                            input_place_ids = [], 
                            firing_condition = fc_t_RTN3_exp,
                            reaction_speed_function = r_t_RTN3_exp, 
                            consumption_coefficients = [],
                            output_place_ids = ['p_RTN3_PN'],
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) 
    
        pn.add_transition_with_speed_function(#43
                            transition_id = 't_LE_retro',
                            label = 'retrograde transport of LEs & ER',
                            input_place_ids = ['p_ATP','p_chol_LE','p_RTN3_axon', 'p_tau','p_LRRK2_mut','p_LB'], 
                            firing_condition = fc_t_LE_retro,
                            reaction_speed_function = r_t_LE_retro, 
                            consumption_coefficients = [ATPcons_t_LE_trans, 0, 1, 0,0,0],
                            output_place_ids = ['p_ADP','p_RTN3_PN'],
                            production_coefficients = [ATPcons_t_LE_trans, 1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) 
    
        pn.add_transition_with_speed_function(#44
                            transition_id = 't_LE_antero',
                            label = 'anterograde transport of LEs & ER',
                            input_place_ids = ['p_ATP','p_RTN3_PN', 'p_tau'], # didn't connect p_tau yet
                            firing_condition = fc_t_LE_antero,
                            reaction_speed_function = r_t_LE_antero, # get later from NPCD
                            consumption_coefficients = [ATPcons_t_LE_trans, 1, 0], # tune these coefficients based on PD
                            output_place_ids = ['p_ADP','p_RTN3_axon'],
                            production_coefficients = [ATPcons_t_LE_trans, 1],# tune these coefficients based on PD
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect)  
    
        pn.add_transition_with_speed_function(#45
                            transition_id = 't_RTN3_aggregation',
                            label = 'aggregation of monomeric RTN3 into HMW RTN3',
                            input_place_ids = ['p_RTN3_axon', 'p_RTN3_PN'], 
                            firing_condition = fc_t_RTN3_aggregation, # tune aggregation limit later
                            reaction_speed_function = r_t_RTN3_aggregation,
                            consumption_coefficients = [1, 1],
                            output_place_ids = ['p_RTN3_HMW_cyto'],
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) 
    
        pn.add_transition_with_speed_function(#46
                            transition_id = 't_RTN3_auto',
                            label = 'functional autophagy of HMW RTN3',
                            input_place_ids = ['p_RTN3_HMW_cyto', 'p_RTN3_axon'], 
                            firing_condition = fc_t_RTN3_auto, 
                            reaction_speed_function = r_t_RTN3_auto,
                            consumption_coefficients = [1, 0],
                            output_place_ids = ['p_RTN3_HMW_auto'],
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) 
    
        pn.add_transition_with_speed_function(#47
                            transition_id = 't_RTN3_lyso',
                            label = 'functional delivery of HMW RTN3 to the lysosome',
                            input_place_ids = ['p_RTN3_HMW_auto', 'p_tau'], 
                            firing_condition = fc_t_RTN3_lyso, 
                            reaction_speed_function = r_t_RTN3_lyso,
                            consumption_coefficients = [1, 0],
                            output_place_ids = ['p_RTN3_HMW_lyso'],
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) 
    
        pn.add_transition_with_speed_function(#48
                            transition_id = 't_RTN3_dys_auto',
                            label = 'dysfunctional autophagy of HMW RTN3',
                            input_place_ids = ['p_RTN3_HMW_cyto', 'p_RTN3_axon'], 
                            firing_condition = fc_t_RTN3_dys_auto, 
                            reaction_speed_function = r_t_RTN3_dys_auto,
                            consumption_coefficients = [1, 0],
                            output_place_ids = ['p_RTN3_HMW_dys1'],
                            production_coefficients = [1],# tune later when data are incorporated
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect)  
    
        pn.add_transition_with_speed_function(#49
                            transition_id = 't_RTN3_dys_lyso',
                            label = 'dysfunctional delivery of HMW RTN3 to the lysosome',
                            input_place_ids = ['p_RTN3_HMW_auto', 'p_RTN3_HMW_dys1', 'p_tau'], 
                            firing_condition = fc_t_RTN3_dys_lyso, 
                            reaction_speed_function = r_t_RTN3_dys_lyso,
                            consumption_coefficients = [1, 0, 0],
                            output_place_ids = ['p_RTN3_HMW_dys2'],
                            production_coefficients = [1],# tune later when data are incorporated
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) 
        pn.add_transition_with_speed_function(#50
                            transition_id = 't_MDV_Generation_basal',
                            label = "Mitochondrially Derived Vesicles production",
                            input_place_ids = ['p_chol_mito', 'p_ROS_mito'],
                            firing_condition = lambda a: a['p_chol_mito']>100000,
                            reaction_speed_function = lambda a: 0.0011088*a['p_chol_mito'],
                            consumption_coefficients =[1,0],
                            output_place_ids = ['p_chol_LE'],
                            production_coefficients = [1],
                            stochastic_parameters = [SD, cholSD],
                            collect_rate_analytics = collect_rate_analytics,
                            delay = function_for_MDV_delay) #lambda a: (1/chol_mp)*min(60,max((-24.34*np.log(a['p_ROS_mito'])+309.126)), 20)) #switch: lambda a: 60*(a['p_ROS_mito'] < 80000)+30*(a['p_ROS_mito']>80000)) 
                            
                            
        
        #TESTING ADDED TRANSITION FOR DEBUGGING PURPOSES
        # pn.add_transition_with_speed_function(#50
        #                     transition_id = 'testing',
        #                     label = 'debugging purposes',
        #                     input_place_ids = ['p_RTN3_HMW_auto', 'p_RTN3_HMW_dys1', 'p_tau'], 
        #                     firing_condition = lambda a: True, 
        #                     reaction_speed_function = r_t_RTN3_dys_lyso,
        #                     consumption_coefficients = [1, 0, 0],
        #                     output_place_ids = ['p_RTN3_HMW_dys2', 'p_RTN3_HMW_lyso'],
        #                     production_coefficients = [1, 0],# tune later when data are incorporated
        #                     stochastic_parameters = [SD]) 
        
        # Run the network
        
        frame_in_canvas = self.frame_in_canvas
        
        start_time = datetime.now()
        pn.run_many_times(number_runs=number_runs, number_time_steps=number_time_steps, frame_in_canvas=frame_in_canvas)
        analysis = Analysis(pn)
        execution_time = datetime.now()-start_time
        print('\n\ntime to execute:', execution_time)
        # Save the network
        
        start_time = datetime.now()    
        print("")
        print("Generating Pickle File...")
        print("")
        print("Starting Time is: ", start_time)
        self.button_1.config(text="Generating Pickle File...")
        Analysis.store_to_file(analysis, run_save_name)
        print("")
        print('Network saved to : "' + run_save_name+'.pkl"')
        execution_time = datetime.now()-start_time
        print('\n\nPickling Time:', execution_time) 
        self.button_1.config(text="Restart Session to Re-run")
           
                
               
    def run_AD_sHFPN(self):

                
 #Save Inputs from GUI
        run_save_name = self.HFPN_run_save_name
        number_time_steps = int(self.HFPN_number_of_timesteps)
        time_step_size = float(self.HFPN_timestep_size)
        cholSD = float(self.HFPN_CholSD)
        DelaySD = float(self.HFPN_CalciumSD) 
        it_p_ApoE = self.ApoE4_var.get()
        it_p_CD33 = self.CD33_var.get()
        it_p_age = self.Aged_risk_var.get()
        
        #Disable Run HFPN Button
        self.AD_button_1.config(state=tk.DISABLED)
        self.AD_button_1.config(text="Running Simulation... Please bear with Lag...")
        # Initialize an empty HFPN
        pn = HFPN(time_step = time_step_size) #unit = s/A.U.           
  
            ### Cholesterol Homeostasis
        pn.add_place(it_p_ApoEchol_extra,place_id="p_ApoEchol_extra", label="ApoE-cholesterol complex (extracellular)", continuous=True)
    # Cholesterol in different organelles
        pn.add_place(it_p_chol_LE,place_id="p_chol_LE", label="Cholesterol (late endosome)", continuous=True)
        pn.add_place(it_p_chol_mito,place_id="p_chol_mito", label="Cholesterol (mitochondria)", continuous=True)
        pn.add_place(it_p_chol_ER,place_id="p_chol_ER", label="Cholesterol (ER)", continuous=True)
        pn.add_place(it_p_chol_PM,place_id="p_chol_PM", label="Cholesterol (Plasma Membrane)", continuous=True)
    
        # Oxysterols
        pn.add_place(it_p_24OHchol_extra,place_id="p_24OHchol_extra", label="24-hydroxycholesterol (extracellular)", continuous=True)
        pn.add_place(it_p_24OHchol_intra,place_id="p_24OHchol_intra", label="24-hydroxycholesterol (intracellular)", continuous=True)
        pn.add_place(it_p_27OHchol_extra,place_id="p_27OHchol_extra", label="27-hydroxycholesterol (extracellular)", continuous=True)
        pn.add_place(it_p_27OHchol_intra,place_id="p_27OHchol_intra", label="27-hydroxycholesterol (intracellular)", continuous=True)
        pn.add_place(it_p_7HOCA,place_id="p_7HOCA", label="7-HOCA", continuous=True)
        pn.add_place(it_p_preg,place_id="p_preg", label="Pregnenolon", continuous=True)
        
        ## Tau Places
        pn.add_place(it_p_GSK3b_inact, 'p_GSK3b_inact', 'Inactive GSK3 beta kinase', continuous = True)
        pn.add_place(it_p_GSK3b_act, 'p_GSK3b_act', 'Active GSK3 beta kinase', continuous = True)
        pn.add_place(it_p_tauP, 'p_tauP', 'Phosphorylated tau', continuous = True)
        pn.add_place(it_p_tau, 'p_tau', 'Unphosphorylated tau (microtubule)', continuous = True)

    
        ## AB Places
        pn.add_place(it_p_asec, 'p_asec', 'Alpha secretase', continuous = True)
        pn.add_place(it_p_APP_pm, 'p_APP_pm', 'APP (plasma membrane)', continuous = True) # input
        pn.add_place(it_p_sAPPa, 'p_sAPPa', 'Soluble APP alpha', continuous = True)
        pn.add_place(it_p_CTF83, 'p_CTF83', 'CTF83', continuous = True)
        pn.add_place(it_p_APP_endo, 'p_APP_endo', 'APP (endosome)', continuous = True)
        pn.add_place(it_p_bsec, 'p_bsec', 'Beta secretase', continuous = True)
        pn.add_place(it_p_sAPPb, 'p_sAPPb', 'Soluble APP beta', continuous = True)
        pn.add_place(it_p_CTF99, 'p_CTF99', 'CTF99', continuous = True)
        pn.add_place(it_p_gsec, 'p_gsec', 'Gamma secretase', continuous = True)
        pn.add_place(it_p_AICD, 'p_AICD', 'AICD', continuous = True)
        pn.add_place(it_p_Ab, 'p_Ab', 'Amyloid beta peptide', continuous = True)
        pn.add_place(it_p_ApoE, 'p_ApoE', 'ApoE genotype', continuous = True) # gene, risk factor in AD
        pn.add_place(it_p_age, 'p_age', 'Age risk factor', continuous = True)
        pn.add_place(it_p_CD33, 'p_CD33', 'CD33 mutation', continuous = True) # 80 years old, risk factor in AD for BACE1 activity increase
    # 80 years old, risk factor in AD for BACE1 activity increase
    
        ##AB aggregation places
        pn.add_place(it_p_Ab_elon, place_id="p_Ab_elon", label="Elongating Ab", continuous = True)
        pn.add_place(it_p_Ab_olig, place_id="p_Ab_olig", label="Ab oligomer", continuous = True)
        pn.add_place(it_p_Ab_fib, place_id="p_Ab_fib", label="Ab fibril", continuous = True)
     # ER retraction and collapse
    
        # Monomeric RTN3 (cycling between axonal and perinuclear regions)
        pn.add_place(it_p_RTN3_axon, place_id="p_RTN3_axon", label="Monomeric RTN3 (axonal)", continuous=True)
        pn.add_place(it_p_RTN3_PN, place_id="p_RTN3_PN", label="Monomeric RTN3 (perinuclear)", continuous=True)
    
        # HMW RTN3 (cycling between different cellular compartments)
        pn.add_place(it_p_RTN3_HMW_cyto, place_id="p_RTN3_HMW_cyto", label="HMW RTN3 (cytosol)", continuous=True)
        pn.add_place(it_p_RTN3_HMW_auto, place_id="p_RTN3_HMW_auto", label="HMW RTN3 (autophagosome)", continuous=True)
        pn.add_place(it_p_RTN3_HMW_lyso, place_id="p_RTN3_HMW_lyso", label="HMW RTN3 (degraded in lysosome)", continuous=True)
        pn.add_place(it_p_RTN3_HMW_dys1, place_id="p_RTN3_HMW_dys1", label="HMW RTN3 (type I/III dystrophic neurites)", continuous=True)
        pn.add_place(it_p_RTN3_HMW_dys2, place_id="p_RTN3_HMW_dys2", label="HMW RTN3 (type II dystrophic neurites)", continuous=True)
    
        # Energy metabolism: ATP consumption
        pn.add_place(it_p_ATP, place_id="p_ATP", label="ATP", continuous=True)
        pn.add_place(it_p_ADP, place_id="p_ADP", label="ADP", continuous=True)
        pn.add_place(it_p_cas3, place_id="p_cas3", label="Active caspase 3", continuous=True)
        pn.add_place(it_p_reduc_mito, place_id="p_reduc_mito", label="Reducing agents (mitochondria)", continuous=True)
        pn.add_place(it_p_ROS_mito, place_id="p_ROS_mito", label="ROS (mitochondria)", continuous=True)
        pn.add_place(it_p_H2O_mito, place_id="p_H2O_mito", label="H2O (mitochondria)", continuous=True)

        ##calcium
        
        pn.add_place(it_p_Ca_cyto, "p_Ca_cyto", "Calcium (cytosol)", continuous = True)
        pn.add_place(it_p_Ca_mito, "p_Ca_mito", "Calcium (mitochondria)", continuous = True)
        pn.add_place(it_p_Ca_ER, "p_Ca_ER", "Calcium (ER)", continuous = True)
    
        # Discrete on/of-switches calcium pacemaking
        pn.add_place(1, "p_Ca_extra", "on1 - Calcium (extracellular)", continuous = False)
        pn.add_place(0, "p_on2","on2", continuous = False)
        pn.add_place(0, "p_on3","on3", continuous = False)
        pn.add_place(0, "p_on4","on4", continuous = False)
        
    
        ## Transitions
        # Cholesterol Endocytosis
        pn.add_transition_with_speed_function(
                        transition_id                 = "t_LDLR_endocyto",
                        label                         = "LDLR endocyto",
                        input_place_ids                 = ["p_ApoEchol_extra", "p_chol_ER"],
                        firing_condition             = fc_t_LDLR_endocyto,
                        reaction_speed_function         = r_t_LDLR_endocyto, 
                        consumption_coefficients     = [0,0],
                        output_place_ids             = ["p_chol_LE"], 
                        production_coefficients         = [354],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # Transport Cholesterol from LE to ER
        pn.add_transition_with_speed_function(
                        transition_id                 = "t_chol_trans_LE_ER",
                        label                         = "Chol transport LE-ER",
                        input_place_ids                 = ["p_chol_LE"],
                        firing_condition             = fc_t_chol_trans_LE_ER,
                        reaction_speed_function         = r_t_chol_trans_LE_ER,
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_chol_ER"],
                        production_coefficients         = [1],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # Transport Cholesterol from LE to mito
        pn.add_transition_with_speed_function(
                        transition_id                 = "t_chol_trans_LE_mito",
                        label                         = "Chol transport LE-mito",
                        input_place_ids                 = ["p_chol_LE"],
                        firing_condition             = fc_t_chol_trans_LE_mito,
                        reaction_speed_function         = r_t_chol_trans_LE_mito,
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_chol_mito"],
                        production_coefficients         = [1],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # Transport Cholesterol from LE to PM
        pn.add_transition_with_speed_function(
                        transition_id                 = "t_chol_trans_LE_PM",
                        label                         = "Chol transport LE-PM",
                        input_place_ids                 = ["p_chol_LE"],
                        firing_condition             = fc_t_chol_trans_LE_PM, 
                        reaction_speed_function         = r_t_chol_trans_LE_PM,
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_chol_PM"],
                        production_coefficients         = [1],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # Transport Cholesterol from PM to ER
        pn.add_transition_with_speed_function(
                        transition_id                 = "t_chol_trans_PM_ER",
                        label                         = "Chol transport PM-ER",
                        input_place_ids                 = ["p_chol_PM"],
                        firing_condition             = fc_t_chol_trans_PM_ER,
                        reaction_speed_function         = r_t_chol_trans_PM_ER,
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_chol_ER"],
                        production_coefficients         = [1],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # Transport Cholesterol from ER to PM
        pn.add_transition_with_speed_function(
                        transition_id                 = "t_chol_trans_ER_PM",
                        label                         = "Chol transport ER-PM",
                        input_place_ids                 = ["p_chol_ER"],
                        firing_condition             = fc_t_chol_trans_ER_PM,
                        reaction_speed_function         = r_t_chol_trans_ER_PM,
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_chol_PM"],
                        production_coefficients         = [1],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # Transport Cholesterol from ER to mito
        pn.add_transition_with_speed_function(
                        transition_id                 = "t_chol_trans_ER_mito",
                        label                         = "Chol transport ER-mito",
                        input_place_ids                 = ["p_chol_ER"],
                        firing_condition             = fc_t_chol_trans_ER_mito,
                        reaction_speed_function         = r_t_chol_trans_ER_mito,
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_chol_mito"],
                        production_coefficients         = [1],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # Metabolisation of chol by CYP27A1
        pn.add_transition_with_michaelis_menten(
                        transition_id                 = "t_CYP27A1_metab",
                        label                         = "Chol metab CYP27A1",
                        Km                             = Km_t_CYP27A1_metab,
                        vmax                         = vmax_t_CYP27A1_metab,
                        input_place_ids                 = ["p_chol_mito"],
                        substrate_id                 = "p_chol_mito",
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_27OHchol_intra"],
                        production_coefficients         = [1],
                        vmax_scaling_function         = vmax_scaling_t_CYP27A1_metab,
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # Metabolism of chol by CYP11A1
        pn.add_transition_with_michaelis_menten(
                        transition_id                 = "t_CYP11A1_metab",
                        label                         = "Chol metab CYP11A1",
                        Km                             = Km_t_CYP11A1_metab,
                        vmax                         = vmax_t_CYP11A1_metab,
                        input_place_ids                 = ["p_chol_mito"],
                        substrate_id                 = "p_chol_mito",
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_preg"],
                        production_coefficients         = [1],
                        vmax_scaling_function         = vmax_scaling_t_CYP11A1_metab,
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # Metabolisation of 27OHchol by CYP7B1
        pn.add_transition_with_michaelis_menten(
                        transition_id                 = "t_CYP7B1_metab",
                        label                         = "27OHchol metab CYP7B1",
                        Km                             = Km_t_CYP7B1_metab,
                        vmax                         = vmax_t_CYP7B1_metab,
                        input_place_ids                 = ["p_27OHchol_intra"],
                        substrate_id                 = "p_27OHchol_intra",
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_7HOCA"],
                        production_coefficients         = [1],
                        vmax_scaling_function         = vmax_scaling_t_CYP7B1_metab,
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # Endocytosis of 27OHchol
        pn.add_transition_with_speed_function(
                        transition_id                 = "t_27OHchol_endocyto",
                        label                         = "27OHchol endocyto",
                        input_place_ids                 = ["p_27OHchol_extra"],
                        firing_condition             = fc_t_27OHchol_endocyto,
                        reaction_speed_function         = r_t_27OHchol_endocyto,
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_27OHchol_intra", "p_27OHchol_extra"],
                        production_coefficients         = [1,1],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # Metabolisation of chol by CYP46A1
        pn.add_transition_with_michaelis_menten(
                        transition_id                 = "t_CYP46A1_metab",
                        label                         = "Chol metab CYP46A1",
                        Km                             = Km_t_CYP46A1_metab,
                        vmax                         = vmax_t_CYP46A1_metab,
                        input_place_ids                 = ["p_chol_ER"],
                        substrate_id                 = "p_chol_ER",
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_24OHchol_intra"],
                        production_coefficients         = [1],
                        vmax_scaling_function         = vmax_scaling_t_CYP46A1_metab,
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # Exocytosis of 24OHchol
        pn.add_transition_with_speed_function(
                        transition_id                 = "t_24OHchol_exocyto",
                        label                         = "24OHchol exocyto",
                        input_place_ids                 = ["p_24OHchol_intra"],
                        firing_condition             = fc_t_24OHchol_exocyto,
                        reaction_speed_function         = r_t_24OHchol_exocyto,
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_24OHchol_extra"],
                        production_coefficients         = [1],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
        # Transport of Chol into ECM
        pn.add_transition_with_speed_function(
                        transition_id                 = "t_chol_trans_PM_ECM",
                        label                         = "Chol transport PM-ECM",
                        input_place_ids                 = ["p_chol_PM", "p_24OHchol_intra"],
                        firing_condition             = fc_t_chol_trans_PM_ECM,
                        reaction_speed_function         = r_t_chol_trans_PM_ECM,
                        consumption_coefficients     = [1,0],
                        output_place_ids             = [],
                        production_coefficients         = [],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = collect_rate_analytics)
    
    #tau
        ## Transitions
        pn.add_transition_with_speed_function(
                        transition_id                 = 't_GSK3b_exp_deg',
                        label                         = 'GSK3beta expression and degradation',
                        input_place_ids                 = ['p_GSK3b_inact'], 
                        firing_condition             = fc_t_GSK3b_exp_deg,
                        reaction_speed_function         = r_t_GSK3b_exp_deg,
                        consumption_coefficients     = [0], 
                        output_place_ids             = ['p_GSK3b_inact'],
                        production_coefficients         = [1],
                        stochastic_parameters = [SD],
                        collect_rate_analytics = collect_rate_analytics)
    
        pn.add_transition_with_speed_function(
                        transition_id                 = 't_actv_GSK3b',
                        label                         = 'GSK3beta activation',
                        input_place_ids                 = ['p_GSK3b_inact', 'p_ApoE', 'p_Ab'], 
                        firing_condition             = fc_t_actv_GSK3b,
                        reaction_speed_function         = r_t_actv_GSK3b,
                        consumption_coefficients     = [1, 0, 0], 
                        output_place_ids             = ['p_GSK3b_act'],
                        production_coefficients         = [1],
                        stochastic_parameters = [SD],
                        collect_rate_analytics = collect_rate_analytics)
    
    
        pn.add_transition_with_speed_function(
                        transition_id                 = 't_inactv_GSK3b',
                        label                         = 'GSK3beta inactivation',
                        input_place_ids                 = ['p_GSK3b_act'], 
                        firing_condition             = fc_t_inactv_GSK3b, 
                        reaction_speed_function         = r_t_inactv_GSK3b,
                        consumption_coefficients     = [1], 
                        output_place_ids             = ['p_GSK3b_inact'],
                        production_coefficients         = [1],
                        stochastic_parameters = [SD],
                        collect_rate_analytics = collect_rate_analytics)
            

        pn.add_transition_with_michaelis_menten(
                        transition_id                 = 't_phos_tau',
                        label                         = 'Phosphorylation of tau',
                        Km                             = Km_t_phos_tau, 
                        vmax                         = kcat_t_phos_tau, 
                        input_place_ids                 = ['p_tau', 'p_GSK3b_act', 'p_cas3'],
                        substrate_id                 = 'p_tau',
                        consumption_coefficients     = [1, 0, 0],
                        output_place_ids             = ['p_tauP'],
                        production_coefficients         = [1],
                        vmax_scaling_function         = vmax_scaling_t_phos_tau,
                        stochastic_parameters = [SD],
                        collect_rate_analytics = collect_rate_analytics)
    
    
        pn.add_transition_with_michaelis_menten(
                        transition_id                 = 't_dephos_tauP',
                        label                         = 'Dephosphorylation of tau protein',
                        Km                             = Km_t_dephos_tauP, 
                        vmax                         = vmax_t_dephos_tauP, 
                        input_place_ids                 = ['p_tauP', 'p_Ca_cyto'],
                        substrate_id                 = 'p_tauP',
                        consumption_coefficients     = [1, 0],
                        output_place_ids             = ['p_tau'],
                        production_coefficients         = [1],
                        vmax_scaling_function         = vmax_scaling_t_dephos_tauP,
                        stochastic_parameters = [SD],
                        collect_rate_analytics = collect_rate_analytics)
    
    
    
        ## AB Transitions
        pn.add_transition_with_michaelis_menten(
                        transition_id                 = 't_APP_asec_cleav',
                        label                         = 'Alpha cleavage of APP',
                        Km = Km_t_APP_asec_cleav, 
                        vmax = kcat_t_APP_asec_cleav,
                        input_place_ids                 = ['p_APP_pm', 'p_asec', 'p_chol_PM'],
                        substrate_id = 'p_APP_pm', 
                        consumption_coefficients     = [1, 0, 0],
                        output_place_ids = ['p_sAPPa', 'p_CTF83'],
                        production_coefficients = [1, 1],
                        vmax_scaling_function = vmax_scaling_t_APP_asec_cleav,
                        stochastic_parameters = [SD],
                        collect_rate_analytics = collect_rate_analytics)
    
        pn.add_transition_with_speed_function(
                        transition_id                 = 't_asec_exp',
                        label                         = 'Alpha secretase expression',
                        input_place_ids                 = ['p_24OHchol_intra'],
                        firing_condition             = fc_t_asec_exp,
                        reaction_speed_function         = r_t_asec_exp,
                        consumption_coefficients     = [0], 
                        output_place_ids = ['p_asec'], # none
                        production_coefficients = [1],
                        stochastic_parameters = [SD],
                        collect_rate_analytics = collect_rate_analytics)
        
        pn.add_transition_with_speed_function(
                        transition_id                 = 't_asec_degr',
                        label                         = 'Alpha secretase degradation',
                        input_place_ids                 = ['p_asec'],
                        firing_condition             = fc_t_asec_degr,
                        reaction_speed_function         = r_t_asec_degr,
                        consumption_coefficients     = [1], 
                        output_place_ids = [], # none
                        production_coefficients = [],
                        stochastic_parameters = [SD],
                        collect_rate_analytics = collect_rate_analytics)# none
    
        pn.add_transition_with_speed_function(
                        transition_id                 = 't_APP_exp',
                        label                         = 'APP expression rate',
                        input_place_ids                 = ['p_ApoE', 'p_ROS_mito'],
                        firing_condition             = fc_t_APP_exp,
                        reaction_speed_function         = r_t_APP_exp,
                        consumption_coefficients     = [0, 0], 
                        output_place_ids = ['p_APP_pm'],
                        production_coefficients = [1],
                        stochastic_parameters = [SD],
                        collect_rate_analytics = collect_rate_analytics)
    
        pn.add_transition_with_speed_function(
                        transition_id                 = 't_APP_endocyto',
                        label                         = 'endocytosis',
                        input_place_ids                 = ['p_APP_pm', 'p_ApoE'], 
                        firing_condition             = fc_t_APP_endocyto,
                        reaction_speed_function         = r_t_APP_endocyto,
                        consumption_coefficients     = [1, 0], 
                        output_place_ids = ['p_APP_endo'],
                        production_coefficients = [1],
                        stochastic_parameters = [SD],
                        collect_rate_analytics = collect_rate_analytics)
        
        pn.add_transition_with_speed_function(
                        transition_id                 = 't_APP_endo_event',
                        label                         = 'APP-utilizing cellular events',
                        input_place_ids                 = ['p_APP_endo'], 
                        firing_condition             = fc_t_APP_endo_event,
                        reaction_speed_function         = r_t_APP_endo_event,
                        consumption_coefficients     = [1], 
                        output_place_ids = [],
                        production_coefficients = [],
                        stochastic_parameters = [SD],
                        collect_rate_analytics = collect_rate_analytics)
    
        pn.add_transition_with_michaelis_menten(
                        transition_id                 = 't_APP_bsec_cleav',
                        label                         = 'Beta cleavage of APP',
                        Km = Km_t_APP_bsec_cleav, 
                        vmax = kcat_t_APP_bsec_cleav,
                        input_place_ids                 = ['p_APP_endo', 'p_bsec', 'p_chol_PM', 'p_age'],
                        substrate_id = 'p_APP_endo', 
                        consumption_coefficients     = [1, 0, 0, 0],
                        output_place_ids = ['p_sAPPb', 'p_CTF99'],
                        production_coefficients = [1, 1],
                        vmax_scaling_function = vmax_scaling_t_APP_bsec_cleav,
                        stochastic_parameters = [SD],
                        collect_rate_analytics = collect_rate_analytics)
    
        pn.add_transition_with_speed_function(
                        transition_id                 = 't_bsec_exp',
                        label                         = 'Beta secretase expression',
                        input_place_ids                 = ['p_ROS_mito', 'p_27OHchol_intra', 'p_RTN3_axon'],
                        firing_condition             = fc_t_bsec_exp,
                        reaction_speed_function         = r_t_bsec_exp, 
                        consumption_coefficients     = [0, 0, 0], 
                        output_place_ids = ['p_bsec'], # none
                        production_coefficients = [1],
                        stochastic_parameters = [SD],
                        collect_rate_analytics = collect_rate_analytics)# none
        
        pn.add_transition_with_speed_function(
                        transition_id                 = 't_bsec_degr',
                        label                         = 'Beta secretase degradation',
                        input_place_ids                 = ['p_bsec'],
                        firing_condition             = fc_t_bsec_degr,
                        reaction_speed_function         = r_t_bsec_degr, 
                        consumption_coefficients     = [1], 
                        output_place_ids = [], # none
                        production_coefficients = [],
                        stochastic_parameters = [SD],
                        collect_rate_analytics = collect_rate_analytics)# none
    
        pn.add_transition_with_michaelis_menten(
                        transition_id                 = 't_CTF99_gsec_cleav',
                        label                         = 'Gamma secretase cleavage of CTF99',
                        Km = Km_t_CTF99_gsec_cleav, 
                        vmax = kcat_t_CTF99_gsec_cleav,
                        input_place_ids                 = ['p_CTF99', 'p_gsec', 'p_chol_PM'],
                        substrate_id = 'p_CTF99', 
                        consumption_coefficients     = [1, 0, 0],
                        output_place_ids = ['p_Ab', 'p_AICD'],
                        production_coefficients = [1, 1],
                        vmax_scaling_function = vmax_scaling_t_CTF99_gsec_cleav,
                        stochastic_parameters = [SD],
                        collect_rate_analytics = collect_rate_analytics)
    
        pn.add_transition_with_speed_function(
                        transition_id                 = 't_gsec_exp',
                        label                         = 'Gamma secretase expression',
                        input_place_ids                 = ['p_ROS_mito'],
                        firing_condition             = fc_t_gsec_exp,
                        reaction_speed_function         = r_t_gsec_exp, 
                        consumption_coefficients     = [0], 
                        output_place_ids = ['p_gsec'], 
                        production_coefficients = [1],
                        stochastic_parameters = [SD],
                        collect_rate_analytics = collect_rate_analytics)
        
        pn.add_transition_with_speed_function(
                        transition_id                 = 't_gsec_degr',
                        label                         = 'Gamma secretase degradation',
                        input_place_ids                 = ['p_gsec'],
                        firing_condition             = fc_t_gsec_degr,
                        reaction_speed_function         = r_t_gsec_degr, 
                        consumption_coefficients     = [1], 
                        output_place_ids = [], # none
                        production_coefficients = [],
                        stochastic_parameters = [SD],
                        collect_rate_analytics = collect_rate_analytics)# none
    
        pn.add_transition_with_speed_function(
                        transition_id                 = 't_Ab_degr',
                        label                         = 'Ab degradation',
                        input_place_ids                 = ['p_Ab'], 
                        firing_condition             = fc_t_Ab_degr,
                        reaction_speed_function         = r_t_Ab_degr,
                        consumption_coefficients     = [1], 
                        output_place_ids = [],
                        production_coefficients = [],
                        stochastic_parameters = [SD],
                        collect_rate_analytics = collect_rate_analytics)# TODO - fix ratio
    
        pn.add_transition_with_speed_function(
                        transition_id                 = 't_Ab_phag',
                        label                         = 'Ab phagocytosis',
                        input_place_ids                 = ['p_Ab'], 
                        firing_condition             = fc_t_Ab_phag,
                        reaction_speed_function         = r_t_Ab_phag,
                        consumption_coefficients     = [1], 
                        output_place_ids = [],
                        production_coefficients = [],
                        stochastic_parameters = [SD],
                        collect_rate_analytics = collect_rate_analytics)# TODO - fix ratio
    
    ##AB aggregation module
      ##AB Aggregation transitions
            
        pn.add_transition_with_speed_function(transition_id = 't_Ab_elon',
                            label                = "Ab elongation step",
                            input_place_ids       = ['p_Ab'],
                            firing_condition = fc_t_Ab_elon,
                            reaction_speed_function = r_t_Ab_elon,
                            consumption_coefficients  = [1], 
                            output_place_ids       = ['p_Ab_elon'],
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
        
        pn.add_transition_with_speed_function(transition_id = 't_Ab_agg',
                            label                = "Ab aggregation",
                            input_place_ids       = ['p_Ab_elon'],
                            firing_condition = fc_t_Ab_agg,
                            reaction_speed_function = r_t_Ab_agg,
                            consumption_coefficients  = [12.4], 
                            output_place_ids       = ['p_Ab_olig'],
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
    
        pn.add_transition_with_speed_function(transition_id = 't_Ab_fib',
                            label                = "Ab fibrillation",
                            input_place_ids       = ['p_Ab_olig'],
                            firing_condition = fc_t_Ab_fib,
                            reaction_speed_function = r_t_Ab_fib,
                            consumption_coefficients  = [4], 
                            output_place_ids       = ['p_Ab_fib'],
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
        
        pn.add_transition_with_speed_function(transition_id = 't_Ab_frag',
                            label                = "Ab fragmentation",
                            input_place_ids       = ['p_Ab_fib'],
                            firing_condition = fc_t_Ab_frag,
                            reaction_speed_function = r_t_Ab_frag,
                            consumption_coefficients  = [1], 
                            output_place_ids       = ['p_Ab_olig', 'p_Ab'],
                            production_coefficients = [3,12.4],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
    
        pn.add_transition_with_speed_function(transition_id = 't_Abfib_phag',
                            label                = "Ab fibril phagocytosis",
                            input_place_ids       = ['p_Ab_fib'],
                            firing_condition = fc_t_Abfib_phag,
                            reaction_speed_function = r_t_Abfib_phag,
                            consumption_coefficients  = [1], 
                            output_place_ids       = [],
                            production_coefficients = [],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
            
        
    
        pn.add_transition_with_speed_function(
                            transition_id = 't_RTN3_exp',
                            label = 'Expression rate of RTN3',
                            input_place_ids = [], 
                            firing_condition = fc_t_RTN3_exp,
                            reaction_speed_function = r_t_RTN3_exp, 
                            consumption_coefficients = [],
                            output_place_ids = ['p_RTN3_PN'],
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
        
        pn.add_transition_with_speed_function(
                            transition_id = 't_LE_retro',
                            label = 'retrograde transport of LEs & ER',
                            input_place_ids = ['p_ATP','p_chol_LE','p_RTN3_axon', 'p_tau'], # didn't connect p_tau or p_chol_LE yet
                            firing_condition = fc_t_LE_retro,
                            reaction_speed_function = r_t_LE_retro, # get later from PD
                            consumption_coefficients = [ATPcons_t_LE_trans, 0, 1, 0], # tune these coefficients based on PD
                            output_place_ids = ['p_ADP','p_RTN3_PN'],
                            production_coefficients = [ATPcons_t_LE_trans, 1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)# tune these coefficients based on PD
    
        pn.add_transition_with_speed_function(
                            transition_id = 't_LE_antero',
                            label = 'anterograde transport of LEs & ER',
                            input_place_ids = ['p_ATP','p_RTN3_PN', 'p_tau'], # didn't connect p_tau yet
                            firing_condition = fc_t_LE_antero,
                            reaction_speed_function = r_t_LE_antero, # get later from NPCD
                            consumption_coefficients = [ATPcons_t_LE_trans, 1, 0], # tune these coefficients based on PD
                            output_place_ids = ['p_ADP','p_RTN3_axon'],
                            production_coefficients = [ATPcons_t_LE_trans, 1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)# tune these coefficients based on PD
    
        pn.add_transition_with_speed_function(
                            transition_id = 't_RTN3_aggregation',
                            label = 'aggregation of monomeric RTN3 into HMW RTN3',
                            input_place_ids = ['p_RTN3_axon', 'p_RTN3_PN', 'p_Ab'], 
                            firing_condition = fc_t_RTN3_aggregation, # tune aggregation limit later
                            reaction_speed_function = r_t_RTN3_aggregation,
                            consumption_coefficients = [1, 1, 0],
                            output_place_ids = ['p_RTN3_HMW_cyto'],
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
    
        pn.add_transition_with_speed_function(
                            transition_id = 't_RTN3_auto',
                            label = 'functional autophagy of HMW RTN3',
                            input_place_ids = ['p_RTN3_HMW_cyto', 'p_RTN3_axon'], 
                            firing_condition = fc_t_RTN3_auto, 
                            reaction_speed_function = r_t_RTN3_auto,
                            consumption_coefficients = [1, 0],
                            output_place_ids = ['p_RTN3_HMW_auto'],
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
    
        pn.add_transition_with_speed_function(
                            transition_id = 't_RTN3_lyso',
                            label = 'functional delivery of HMW RTN3 to the lysosome',
                            input_place_ids = ['p_RTN3_HMW_auto', 'p_tau'], 
                            firing_condition = fc_t_RTN3_lyso, 
                            reaction_speed_function = r_t_RTN3_lyso,
                            consumption_coefficients = [1, 0],
                            output_place_ids = ['p_RTN3_HMW_lyso'],
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
    
        pn.add_transition_with_speed_function(
                            transition_id = 't_RTN3_dys_auto',
                            label = 'dysfunctional autophagy of HMW RTN3',
                            input_place_ids = ['p_RTN3_HMW_cyto', 'p_RTN3_axon'], 
                            firing_condition = fc_t_RTN3_dys_auto, 
                            reaction_speed_function = r_t_RTN3_dys_auto,
                            consumption_coefficients = [1, 0],
                            output_place_ids = ['p_RTN3_HMW_dys1'],
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)# tune later when data are incorporated
    
        pn.add_transition_with_speed_function(
                            transition_id = 't_RTN3_dys_lyso',
                            label = 'dysfunctional delivery of HMW RTN3 to the lysosome',
                            input_place_ids = ['p_RTN3_HMW_auto', 'p_RTN3_HMW_dys1', 'p_tau'], 
                            firing_condition = fc_t_RTN3_dys_lyso, 
                            reaction_speed_function = r_t_RTN3_dys_lyso,
                            consumption_coefficients = [1, 0, 0],
                            output_place_ids = ['p_RTN3_HMW_dys2'],
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)# tune later when 
      
        
        # Transitions
        pn.add_transition_with_speed_function(  
                    transition_id = 't_krebs', 
                    label = 'Krebs cycle', 
                    input_place_ids = ['p_ADP', 'p_Ca_mito', "p_Ab"],
                    firing_condition = fc_t_krebs,
                    reaction_speed_function = r_t_krebs,
                    consumption_coefficients = [1, 0, 0],
                    output_place_ids = ['p_reduc_mito', 'p_ATP'], 
                    production_coefficients = [4,1],
                    stochastic_parameters = [SD],
                    collect_rate_analytics = collect_rate_analytics)
        
        pn.add_transition_with_speed_function(  
                    transition_id = 't_ATP_hydro_mito', 
                    label = 'ATP hydrolysis by cellular processes', 
                    input_place_ids = ['p_ATP'],
                    firing_condition = fc_t_ATP_hydro_mito,
                    reaction_speed_function = r_t_ATP_hydro_mito,
                    consumption_coefficients = [1],
                    output_place_ids = ['p_ADP'], 
                    production_coefficients = [1],
                    stochastic_parameters = [SD],
                    collect_rate_analytics = collect_rate_analytics)
        
        pn.add_transition_with_speed_function(  
                    transition_id = 't_ETC', 
                    label = 'Electron transport chain', 
                    input_place_ids = ['p_reduc_mito', 'p_ADP', 'p_Ca_mito', 'p_ROS_mito', 'p_chol_mito', "p_Ab"],
                    firing_condition = fc_t_ETC,
                    reaction_speed_function = r_t_ETC,
                    consumption_coefficients = [22/3.96, 440, 0, 0, 0, 0],
                    output_place_ids = ['p_ATP', 'p_ROS_mito'], 
                    production_coefficients = [440, 0.06],
                    stochastic_parameters = [SD],
                    collect_rate_analytics = collect_rate_analytics)
        
        pn.add_transition_with_speed_function(  
                    transition_id = 't_ROS_metab', 
                    label = 'Neutralization of ROS', 
                    input_place_ids = ['p_ROS_mito', 'p_chol_mito'],
                    firing_condition = fc_t_ROS_metab,
                    reaction_speed_function = r_t_ROS_metab,
                    consumption_coefficients = [1, 0],
                    output_place_ids = ['p_H2O_mito'], 
                    production_coefficients = [1],
                    stochastic_parameters = [SD],
                    collect_rate_analytics = collect_rate_analytics)
    
        # Output transitions: Cas3 for apoptosis
        pn.add_transition_with_speed_function(
                            transition_id = 't_mito_dysfunc',
                            label = 'Mitochondrial complex 1 dysfunction',
                            input_place_ids = ['p_ROS_mito','p_Ab'],
                            firing_condition = fc_t_mito_dysfunc,
                            reaction_speed_function = r_t_mito_dysfunc,
                            consumption_coefficients = [1,0], 
                            output_place_ids = ['p_cas3'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
        # Cas3 inactivation
        pn.add_transition_with_speed_function(
                            transition_id = 't_cas3_inact',
                            label = 'Caspase 3 inactivation',
                            input_place_ids = ['p_cas3'],
                            firing_condition = fc_t_cas3_inact,
                            reaction_speed_function = r_t_cas3_inact,
                            consumption_coefficients = [1], 
                            output_place_ids = [],         
                            production_coefficients = [],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
        
        pn.add_transition_with_speed_function(
                            transition_id = 't_ROS_gener_Ab',
                            label = 'ROS generation by Abeta',
                            input_place_ids = ['p_Ab'],
                            firing_condition = fc_t_ROS_gener_Ab,
                            reaction_speed_function = r_t_ROS_gener_Ab,
                            consumption_coefficients = [0], 
                            output_place_ids = ["p_ROS_mito"],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
    
    
    
    
      
    
        # Add transitions
        pn.add_transition_with_speed_function(
                            transition_id = 't_Ca_imp',
                            label = 'VGCC/NMDA import channels',
                            input_place_ids = ['p_Ca_extra'],
                            firing_condition = fc_t_Ca_imp,
                            reaction_speed_function = r_t_Ca_imp,
                            consumption_coefficients = [0],  
                            output_place_ids = ['p_Ca_cyto'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
    
        pn.add_transition_with_speed_function(
                            transition_id = 't_mCU',
                            label = 'Ca import into mitochondria via mCU',
                            input_place_ids = ['p_Ca_cyto', 'p_Ca_mito'],
                            firing_condition = fc_t_mCU,
                            reaction_speed_function = r_t_mCU,
                            consumption_coefficients = [1,0], 
                            output_place_ids = ['p_Ca_mito'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
    
        pn.add_transition_with_speed_function(
                            transition_id = 't_MAM',
                            label = 'Ca transport from ER to mitochondria',
                            input_place_ids = ['p_Ca_ER', 'p_Ca_mito'],
                            firing_condition = fc_t_MAM,
                            reaction_speed_function = r_t_MAM,
                            consumption_coefficients = [1,0], 
                            output_place_ids = ['p_Ca_mito'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
                            
    
        pn.add_transition_with_speed_function(
                            transition_id = 't_RyR_IP3R',
                            label = 'Ca export from ER',
                            input_place_ids = ['p_Ca_extra', 'p_Ca_ER'],
                            firing_condition = fc_t_RyR_IP3R,
                            reaction_speed_function = r_t_RyR_IP3R,
                            consumption_coefficients = [0,1], 
                            output_place_ids = ['p_Ca_cyto'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
    
        pn.add_transition_with_speed_function(
                            transition_id = 't_SERCA',
                            label = 'Ca import to ER',
                            input_place_ids = ['p_Ca_cyto','p_ATP'],
                            firing_condition = fc_t_SERCA,
                            reaction_speed_function = r_t_SERCA,
                            consumption_coefficients = [1,0.5], 
                            output_place_ids = ['p_Ca_ER','p_ADP'],         
                            production_coefficients = [1,0.5],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
    
        pn.add_transition_with_speed_function(
                            transition_id = 't_NCX_PMCA',
                            label = 'Ca efflux to extracellular space',
                            input_place_ids = ['p_Ca_cyto','p_on3'],
                            firing_condition = lambda a: a['p_on3']==1,
                            reaction_speed_function = r_t_NCX_PMCA,
                            consumption_coefficients = [1,0], 
                            output_place_ids = [],         
                            production_coefficients = [],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
        
        pn.add_transition_with_speed_function(
                            transition_id = 't_mNCLX',
                            label = 'Ca export from mitochondria via mNCLX',
                            input_place_ids = ['p_Ca_mito'],
                            firing_condition = fc_t_mNCLX,
                            reaction_speed_function = r_t_mNCLX,
                            consumption_coefficients = [1], 
                            output_place_ids = ['p_Ca_cyto'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
    
        # Discrete on/of-switches calcium pacemaking
        pn.add_transition_with_speed_function(
                            transition_id = 't_A',
                            label = 'A',
                            input_place_ids = ['p_on4'],
                            firing_condition = lambda a: a['p_on4']==1,
                            reaction_speed_function = lambda a: 1,
                            consumption_coefficients = [1], 
                            output_place_ids = ['p_Ca_extra'],         
                            production_coefficients = [1],
                            stochastic_parameters = [CaSD, DelaySD],
                            delay=0.5,
                            collect_rate_analytics = ["no","no"]) 
        
        pn.add_transition_with_speed_function(
                            transition_id = 't_B',
                            label = 'B',
                            input_place_ids = ['p_Ca_extra'],
                            firing_condition = lambda a: a['p_Ca_extra']==1,
                            reaction_speed_function = lambda a: 1,
                            consumption_coefficients = [1], 
                            output_place_ids = ['p_on2'],         
                            production_coefficients = [1],
                            stochastic_parameters = [CaSD, DelaySD],
                            delay=0.5,
                            collect_rate_analytics = ["no","no"]) 
        
        pn.add_transition_with_speed_function(
                            transition_id = 't_C',
                            label = 'C',
                            input_place_ids = ['p_on2'],
                            firing_condition = lambda a: a['p_on2']==1,
                            reaction_speed_function = lambda a: 1,
                            consumption_coefficients = [1], 
                            output_place_ids = ['p_on3'],         
                            production_coefficients = [1],
                            stochastic_parameters = [CaSD, DelaySD],
                            delay=0,
                            collect_rate_analytics = ["no","no"]) 
        
        pn.add_transition_with_speed_function(
                            transition_id = 't_D',
                            label = 'D',
                            input_place_ids = ['p_on3'],
                            firing_condition = lambda a: a['p_on3']==1,
                            reaction_speed_function = lambda a: 1,
                            consumption_coefficients = [1], 
                            output_place_ids = ['p_on4'],         
                            production_coefficients = [1],
                            stochastic_parameters = [CaSD, DelaySD],
                            delay=0.5,
                            collect_rate_analytics = ["no","no"])
    
        # Link to energy metabolism in that it needs ATP replenishment
        pn.add_transition_with_mass_action(
                            transition_id = 't_NaK_ATPase',
                            label = 'NaK ATPase',
                            rate_constant =  k_t_NaK_ATPase,
                            input_place_ids = ['p_ATP', 'p_on3'],
                            firing_condition = lambda a: a['p_on3']==1,
                            consumption_coefficients = [1,0], 
                            output_place_ids = ['p_ADP'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
 
        pn.add_transition_with_speed_function(
                            transition_id = 't_MDV_Generation_basal',
                            label = 't_MDV_Generation_basal',
                            reaction_speed_function =  lambda a : 1,
                            input_place_ids = [],
                            firing_condition = lambda a : True,
                            consumption_coefficients = [], 
                            output_place_ids = [],         
                            production_coefficients = [],
                            stochastic_parameters = [SD, DelaySD],
                            delay=0.5,
                            collect_rate_analytics = collect_rate_analytics)
            
        frame_in_canvas = self.AD_frame_in_canvas
        
        start_time = datetime.now()
        pn.run_many_times(number_runs=number_runs, number_time_steps=number_time_steps, frame_in_canvas=frame_in_canvas)
        analysis = Analysis(pn)
        execution_time = datetime.now()-start_time
        print('\n\ntime to execute:', execution_time)
        # Save the network
        
        start_time = datetime.now()    
        print("")
        print("Generating Pickle File...")
        print("")
        print("Starting Time is: ", start_time)
        self.AD_button_1.config(text="Generating Pickle File...")
        Analysis.store_to_file(analysis, run_save_name)
        print("")
        print('Network saved to : "' + run_save_name+'.pkl"')
        execution_time = datetime.now()-start_time
        print('\n\nPickling Time:', execution_time) 
        self.AD_button_1.config(text="Restart Session to Re-run")
             


 




def main():
    #Initialise GUI
    # root = Tk()
    # root.title("sHFPN GUI")
    # root.geometry("700x600")
    
    # main_frame = Frame(root)
    # main_frame.pack(fill=BOTH, expand=1)
    
    # #GUI*****Make Menu*****
    # menu = Menu(root)
    # root.config(menu=menu)
    # subMenu = Menu(menu)
    # menu.add_cascade(label="File", menu=subMenu)
    # subMenu.add_command(label="Inputs", command=partial(configure_inputs_file, root, main_frame))
    # subMenu.add_separator()
    



    

    
    # button_2 = Button(root, text="Run Analysis", command=threading.Thread(target = partial(run_Analysis, run_save_name, root, main_frame, second_frame)).start)
    # button_2.pack()
    
    app = sHFPN_GUI_APP()
    app.root.mainloop()   
    
    
def configure_inputs_file(root, main_frame):
    e = Entry(main_frame)
    e.pack()
    button1 = Button(main_frame, text="Enter run_save_name")
    button1.config(command=partial(set_input_file, e, button1))
    button1.pack()
def set_input_file(e, button1):
    input_file_name = e.get()
    global run_save_name
    run_save_name = input_file_name
    print("Input_file_name is now: ", input_file_name)
    button1.destroy()
    e.destroy()    






    
if __name__ == "__main__":
    main()