import os
import sys
import random
import numpy as np
import pandas as pd
import csv
import time
import gc
from IPython import get_ipython

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
# from AD_initial_tokens import *
# from AD_rate_functions import *
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
from tkinter import messagebox
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
import matplotlib.pyplot as plt

class sHFPN_GUI_APP:
    def __init__(self):
        self.root = tk.Tk()
        if platform == 'darwin':
            img = tk.Image("photo", file="mng.png")
            self.root.iconphoto(True, img)
        if platform == 'win32':
            self.root.iconbitmap(r'mngicon.ico')
        self.root.title("sHFPN GUI")
        self.root.geometry("800x680")
        self.Left_Sidebar()
        self.Safe_Exit_Required = False
        
    def Left_Sidebar(self):
        self.frame1= tk.Frame(self.root, width=175)
        self.frame1.pack(side="left", fill=tk.BOTH)
        self.lb = tk.Listbox(self.frame1)
        self.lb['bg']= "black"
        self.lb['fg']= "lime"
        self.lb.pack(side="left", fill=tk.BOTH)
        
        #***Add Different Channels***
        self.lb.insert(tk.END,"", "PD Inputs","AD Inputs", "", "PD Transitions", "AD Transitions", "","Run sHFPN", "Rate Analytics", "Live-Plots", "Live-Rate Plots", "","Analysis", "Saved Runs", "Saved CSVs", "", "About")

        #*** Make Main Frame that other frames will rest on:
        self.frame2= tk.Frame(self.root)
        self.frame2.pack(side="left", fill=tk.BOTH, expand=1)
        self.frame2.grid_rowconfigure(0, weight=1)
        self.frame2.grid_columnconfigure(0, weight=1)

        #Preload PD Places and Transitions
        self.PD_Places()
        self.PD_Continuous_Transitions()
        self.PD_Discrete_Transitions()
        
        #Preload AD Places and Transitions
        # self.AD_Places()
        # self.AD_Continuous_Transitions()
        # self.AD_Discrete_Transitions()
        
        #Preload All GUI Pages
        self.PD_Inputs_Page()
        self.Run_sHFPN_Page()
        self.AD_Inputs_Page()
        self.PD_Transitions_Page()
        # self.AD_Transitions_Page()
        self.Live_Rate_analytics_Page()
        self.Live_Graph()
        self.Live_Graph_Rates()
        self.Analysis_page()
        self.show_saved_runs()
        self.Saved_Csvs_page()
        self.About_Page()
        
        #change the selectbackground of "empty" items to black
        # self.lb.itemconfig(0, selectbackground="black")
        # self.lb.itemconfig(3, selectbackground="black")
        # self.lb.itemconfig(7, selectbackground="black")
        # self.lb.itemconfig(10, selectbackground="black")
        #***Callback Function to execute if items in Left_Sidebars are selected
        def callback(event):
            selection = event.widget.curselection()
            if selection:
                index=selection[0] #selection is a tuple, first item of tuple gives index
                item_name=event.widget.get(index)
                if item_name == "PD Inputs":
                    self.frame3.tkraise()

                if item_name =="AD Inputs":
                    self.AD_frame3.tkraise()
                    
                if item_name == "PD Transitions":
                    self.PD_frame1.tkraise()    
                    
                if item_name == "AD Transitions":
                    self.AD_frame1.tkraise() 
    
                if item_name == "Run sHFPN":
                    self.lb.itemconfig(7,bg="black")
                    self.frame4.tkraise()   
            
                    
                if item_name == "Rate Analytics":
                    self.frame9.tkraise()
                        
                    
                if item_name == "Live-Plots":
                    self.frame8.tkraise()
                    self.lb.itemconfig(9,{'bg':'black'})

                if item_name == "Live-Rate Plots":
                    self.frame10.tkraise()
                    self.lb.itemconfig(10,{'bg':'black'})
                    
                if item_name == "Analysis":
                    self.frame5.tkraise()
                    
                if item_name == "Saved Runs":
                    #Destroy frame to update and remake frame.
                    self.frame6.destroy()
                    self.show_saved_runs()
                    self.frame6.tkraise()
                    
                if item_name == "Saved CSVs":
                    self.frame11.tkraise()
                    
                if item_name == "About":
                    self.frame7.tkraise()
                    
                        
        self.lb.bind("<<ListboxSelect>>", callback)
        
    def Live_Graph_Rates(self):
        self.frame10=tk.Frame(self.frame2)
        self.frame10.grid(row=0, column=0, sticky="nsew")    
        
    def Live_Rate_analytics_Page(self):
        self.frame9 = tk.Frame(self.frame2)
        self.frame9.grid(row=0,column=0, sticky="nsew")
        
        #
        self.PD_rate_canvas = tk.Canvas(self.frame9)
        self.PD_rate_canvas.pack(side="left", fill=tk.BOTH, expand=1)
        
        self.PD_rate_scrollbar = ttk.Scrollbar(self.frame9, orient=tk.VERTICAL, command=self.PD_rate_canvas.yview)
        self.PD_rate_scrollbar.pack(side="left", fill=tk.Y)
        
        self.PD_rate_canvas.configure(yscrollcommand=self.PD_rate_scrollbar.set)
        self.PD_rate_canvas.bind('<Configure>', lambda e: self.PD_rate_canvas.configure(scrollregion= self.PD_rate_canvas.bbox("all")))

        #Create another frame inside the canvas
        self.PD_frame_in_rate_canvas = tk.Frame(self.PD_rate_canvas)
        self.PD_rate_canvas.create_window((0,0), window=self.PD_frame_in_rate_canvas, anchor="nw")         
        #***Select item in Listbox and Display Corresponding output in Right_Output
        #self.lb.bind("<<ListboxSelect>>", Lambda x: show)


    def AD_Transitions_Page(self):
        self.AD_frame1 = tk.Frame(self.frame2)
        self.AD_frame1.grid(row=0,column=0,sticky="nsew")
        self.AD_trans_canvas = tk.Canvas(self.AD_frame1)
        self.AD_trans_canvas.pack(side="left", fill=tk.BOTH, expand=1)
        
        self.AD_trans_scrollbar = ttk.Scrollbar(self.AD_frame1, orient=tk.VERTICAL, command=self.AD_trans_canvas.yview)
        self.AD_trans_scrollbar.pack(side="left", fill=tk.Y)
        
        self.AD_trans_canvas.configure(yscrollcommand=self.AD_trans_scrollbar.set)
        self.AD_trans_canvas.bind('<Configure>', lambda e: self.AD_trans_canvas.configure(scrollregion= self.AD_trans_canvas.bbox("all")))

        #Create another frame inside the canvas
        self.AD_frame_in_canvas = tk.Frame(self.AD_trans_canvas)
        self.AD_trans_canvas.create_window((0,0), window=self.AD_frame_in_canvas, anchor="nw") 
        
        self.AD_transitions_buttons_dict = {}
        self.AD_transitions_entry_box_dict = {}
        self.AD_transitions_consumption_checkboxes_dict = {}
        self.AD_transitions_production_checkboxes_dict = {}

        self.AD_transitions_entry_box_Discrete_SD = {}
        self.AD_consump_checkbox_variables_dict={}     
        self.AD_produc_checkbox_variables_dict={}
        #Headers
        transition_header_button = tk.Button(self.AD_frame_in_canvas, text="Transition", state=tk.DISABLED)
        transition_header_button.grid(row=0, column=1)
        #SD Header
        SD_header_button = tk.Button(self.AD_frame_in_canvas, text="Transition SD", state=tk.DISABLED)
        SD_header_button.grid(row=0, column=2)     
        #DelaySD Header
        DelaySD_header_button = tk.Button(self.AD_frame_in_canvas, text="Delay SD", state=tk.DISABLED)
        DelaySD_header_button.grid(row=0, column=3)
        
        #Collect Rate Analytics Header
        collect_rate_header_button = tk.Button(self.AD_frame_in_canvas, text="Collect Consumption Rate Analytics", state=tk.DISABLED)
        collect_rate_header_button.grid(row=0, column=4)  
        collect_rate_header_button_product = tk.Button(self.AD_frame_in_canvas, text="Collect Production Rate Analytics", state=tk.DISABLED)
        collect_rate_header_button_product.grid(row=0, column=5)  
           
        
        for index, transition in enumerate(self.AD_pn.transitions):
            #dict keys should be the index
            index_str = str(index)
            #Grid Transitions 
            self.AD_transitions_buttons_dict[index_str]=tk.Button(self.AD_frame_in_canvas, text=transition, state=tk.DISABLED)
            self.AD_transitions_buttons_dict[index_str].grid(row=index+1, column=1, pady=10,padx=10)  
            #Transition SD Entry Boxes
            self.AD_transitions_entry_box_dict[index_str] = tk.Entry(self.AD_frame_in_canvas, width=5)
            self.AD_transitions_entry_box_dict[index_str].grid(row=index+1, column=2, pady=10, padx=10)
            default_stochastic_parameter = self.AD_pn.transitions[transition].stochastic_parameters[0] #takes the default stochastic parameter that was preset
            self.AD_transitions_entry_box_dict[index_str].insert(tk.END, default_stochastic_parameter)
            #Checkboxes Collect Rates Consumption
            consump_integer_y_n = self.AD_pn.transitions[transition].collect_rate_analytics[0]
            if consump_integer_y_n == "yes":
                consump_value = 1
            if consump_integer_y_n == "no":
                consump_value = 0
            self.AD_consump_checkbox_variables_dict[index_str] = tk.IntVar(value=consump_value)
            self.AD_transitions_consumption_checkboxes_dict[index_str] = tk.Checkbutton(self.AD_frame_in_canvas, variable=self.AD_consump_checkbox_variables_dict[index_str])
            self.AD_transitions_consumption_checkboxes_dict[index_str].grid(row=index+1, column=4,pady=10, padx=10)
            #Checkboxes Collect Rates Production
            prod_integer_y_n = self.AD_pn.transitions[transition].collect_rate_analytics[1]
            if prod_integer_y_n == "yes":
                prod_value = 1
            if prod_integer_y_n == "no":
                prod_value = 0
            self.AD_produc_checkbox_variables_dict[index_str] = tk.IntVar(value=prod_value)
            self.AD_transitions_production_checkboxes_dict[index_str] = tk.Checkbutton(self.AD_frame_in_canvas, variable=self.AD_produc_checkbox_variables_dict[index_str])
            self.AD_transitions_production_checkboxes_dict[index_str].grid(row=index+1, column=5,pady=10, padx=10)            
            #Collect Rate Analytics Defaul
            
            
            if self.AD_pn.transitions[transition].DiscreteFlag =="yes":
                self.AD_transitions_entry_box_Discrete_SD[index_str] = tk.Entry(self.AD_frame_in_canvas, width=5)
                self.AD_transitions_entry_box_Discrete_SD[index_str].grid(row=index+1, column=3, pady=10, padx=10)
                default_stochastic_parameter = self.AD_pn.transitions[transition].stochastic_parameters[1] #Takes the Discrete Transition Stochastic Parameter now
                self.AD_transitions_entry_box_Discrete_SD[index_str].insert(tk.END, default_stochastic_parameter)        
        
    def PD_Transitions_Page(self):
        self.PD_frame1 = tk.Frame(self.frame2)
        self.PD_frame1.grid(row=0,column=0,sticky="nsew")
        self.PD_trans_canvas = tk.Canvas(self.PD_frame1)
        self.PD_trans_canvas.pack(side="left", fill=tk.BOTH, expand=1)
        
        self.PD_trans_scrollbar = ttk.Scrollbar(self.PD_frame1, orient=tk.VERTICAL, command=self.PD_trans_canvas.yview)
        self.PD_trans_scrollbar.pack(side="left", fill=tk.Y)
        
        self.PD_trans_canvas.configure(yscrollcommand=self.PD_trans_scrollbar.set)
        self.PD_trans_canvas.bind('<Configure>', lambda e: self.PD_trans_canvas.configure(scrollregion= self.PD_trans_canvas.bbox("all")))

        #Create another frame inside the canvas
        self.PD_frame_in_canvas = tk.Frame(self.PD_trans_canvas)
        self.PD_trans_canvas.create_window((0,0), window=self.PD_frame_in_canvas, anchor="nw") 
        
        self.transitions_buttons_dict = {}
        self.transitions_entry_box_dict = {}
        self.transitions_consumption_checkboxes_dict = {}
        self.transitions_production_checkboxes_dict = {}

        self.transitions_entry_box_Discrete_SD = {}
        self.consump_checkbox_variables_dict={}     
        self.produc_checkbox_variables_dict={}
        #Headers
        transition_header_button = tk.Button(self.PD_frame_in_canvas, text="Transition", state=tk.DISABLED)
        transition_header_button.grid(row=0, column=1)
        #SD Header
        SD_header_button = tk.Button(self.PD_frame_in_canvas, text="Transition SD", state=tk.DISABLED)
        SD_header_button.grid(row=0, column=2)     
        #DelaySD Header
        DelaySD_header_button = tk.Button(self.PD_frame_in_canvas, text="Delay SD", state=tk.DISABLED)
        DelaySD_header_button.grid(row=0, column=3)
        
        #Collect Rate Analytics Header
        collect_rate_header_button = tk.Button(self.PD_frame_in_canvas, text="Collect Consumption Rate Analytics", state=tk.DISABLED)
        collect_rate_header_button.grid(row=0, column=4)  
        collect_rate_header_button_product = tk.Button(self.PD_frame_in_canvas, text="Collect Production Rate Analytics", state=tk.DISABLED)
        collect_rate_header_button_product.grid(row=0, column=5)  
           
        
        for index, transition in enumerate(self.PD_pn.transitions):
            #dict keys should be the index
            index_str = str(index)
            #Grid Transitions 
            self.transitions_buttons_dict[index_str]=tk.Button(self.PD_frame_in_canvas, text=transition, state=tk.DISABLED)
            self.transitions_buttons_dict[index_str].grid(row=index+1, column=1, pady=10,padx=10)  
            #Transition SD Entry Boxes
            self.transitions_entry_box_dict[index_str] = tk.Entry(self.PD_frame_in_canvas, width=5)
            self.transitions_entry_box_dict[index_str].grid(row=index+1, column=2, pady=10, padx=10)
            default_stochastic_parameter = self.PD_pn.transitions[transition].stochastic_parameters[0] #takes the default stochastic parameter that was preset
            self.transitions_entry_box_dict[index_str].insert(tk.END, default_stochastic_parameter)
            #Checkboxes Collect Rates Consumption
            consump_integer_y_n = self.PD_pn.transitions[transition].collect_rate_analytics[0]
            if consump_integer_y_n == "yes":
                consump_value = 1
            if consump_integer_y_n == "no":
                consump_value = 0
            self.consump_checkbox_variables_dict[index_str] = tk.IntVar(value=consump_value)
            self.transitions_consumption_checkboxes_dict[index_str] = tk.Checkbutton(self.PD_frame_in_canvas, variable=self.consump_checkbox_variables_dict[index_str])
            self.transitions_consumption_checkboxes_dict[index_str].grid(row=index+1, column=4,pady=10, padx=10)
            #Checkboxes Collect Rates Production
            prod_integer_y_n = self.PD_pn.transitions[transition].collect_rate_analytics[1]
            if prod_integer_y_n == "yes":
                prod_value = 1
            if prod_integer_y_n == "no":
                prod_value = 0
            self.produc_checkbox_variables_dict[index_str] = tk.IntVar(value=prod_value)
            self.transitions_production_checkboxes_dict[index_str] = tk.Checkbutton(self.PD_frame_in_canvas, variable=self.produc_checkbox_variables_dict[index_str])
            self.transitions_production_checkboxes_dict[index_str].grid(row=index+1, column=5,pady=10, padx=10)            
            #Collect Rate Analytics Defaul
            
            
            if self.PD_pn.transitions[transition].DiscreteFlag =="yes":
                self.transitions_entry_box_Discrete_SD[index_str] = tk.Entry(self.PD_frame_in_canvas, width=5)
                self.transitions_entry_box_Discrete_SD[index_str].grid(row=index+1, column=3, pady=10, padx=10)
                default_stochastic_parameter = self.PD_pn.transitions[transition].stochastic_parameters[1] #Takes the Discrete Transition Stochastic Parameter now
                self.transitions_entry_box_Discrete_SD[index_str].insert(tk.END, default_stochastic_parameter)
            
            
    def AD_Places(self):
        self.AD_pn = HFPN()
        
            ### Cholesterol Homeostasis
        self.AD_pn.add_place(it_p_ApoEchol_extra,place_id="p_ApoEchol_extra", label="ApoE-cholesterol complex (extracellular)", continuous=True)
    # Cholesterol in different organelles
        self.AD_pn.add_place(it_p_chol_LE,place_id="p_chol_LE", label="Cholesterol (late endosome)", continuous=True)
        self.AD_pn.add_place(it_p_chol_mito,place_id="p_chol_mito", label="Cholesterol (mitochondria)", continuous=True)
        self.AD_pn.add_place(it_p_chol_ER,place_id="p_chol_ER", label="Cholesterol (ER)", continuous=True)
        self.AD_pn.add_place(it_p_chol_PM,place_id="p_chol_PM", label="Cholesterol (Plasma Membrane)", continuous=True)
    
        # Oxysterols
        self.AD_pn.add_place(it_p_24OHchol_extra,place_id="p_24OHchol_extra", label="24-hydroxycholesterol (extracellular)", continuous=True)
        self.AD_pn.add_place(it_p_24OHchol_intra,place_id="p_24OHchol_intra", label="24-hydroxycholesterol (intracellular)", continuous=True)
        self.AD_pn.add_place(it_p_27OHchol_extra,place_id="p_27OHchol_extra", label="27-hydroxycholesterol (extracellular)", continuous=True)
        self.AD_pn.add_place(it_p_27OHchol_intra,place_id="p_27OHchol_intra", label="27-hydroxycholesterol (intracellular)", continuous=True)
        self.AD_pn.add_place(it_p_7HOCA,place_id="p_7HOCA", label="7-HOCA", continuous=True)
        self.AD_pn.add_place(it_p_preg,place_id="p_preg", label="Pregnenolon", continuous=True)
        
        ## Tau Places
        self.AD_pn.add_place(it_p_GSK3b_inact, 'p_GSK3b_inact', 'Inactive GSK3 beta kinase', continuous = True)
        self.AD_pn.add_place(it_p_GSK3b_act, 'p_GSK3b_act', 'Active GSK3 beta kinase', continuous = True)
        self.AD_pn.add_place(it_p_tauP, 'p_tauP', 'Phosphorylated tau', continuous = True)
        self.AD_pn.add_place(it_p_tau, 'p_tau', 'Unphosphorylated tau (microtubule)', continuous = True)

    
        ## AB Places
        self.AD_pn.add_place(it_p_asec, 'p_asec', 'Alpha secretase', continuous = True)
        self.AD_pn.add_place(it_p_APP_pm, 'p_APP_pm', 'APP (plasma membrane)', continuous = True) # input
        self.AD_pn.add_place(it_p_sAPPa, 'p_sAPPa', 'Soluble APP alpha', continuous = True)
        self.AD_pn.add_place(it_p_CTF83, 'p_CTF83', 'CTF83', continuous = True)
        self.AD_pn.add_place(it_p_APP_endo, 'p_APP_endo', 'APP (endosome)', continuous = True)
        self.AD_pn.add_place(it_p_bsec, 'p_bsec', 'Beta secretase', continuous = True)
        self.AD_pn.add_place(it_p_sAPPb, 'p_sAPPb', 'Soluble APP beta', continuous = True)
        self.AD_pn.add_place(it_p_CTF99, 'p_CTF99', 'CTF99', continuous = True)
        self.AD_pn.add_place(it_p_gsec, 'p_gsec', 'Gamma secretase', continuous = True)
        self.AD_pn.add_place(it_p_AICD, 'p_AICD', 'AICD', continuous = True)
        self.AD_pn.add_place(it_p_Ab, 'p_Ab', 'Amyloid beta peptide', continuous = True)
        self.AD_pn.add_place(it_p_Abconc, 'p_Abconc', 'Amyloid beta peptide concentration', continuous = True)

        self.AD_pn.add_place(it_p_ApoE, 'p_ApoE', 'ApoE genotype', continuous = True) # gene, risk factor in AD
        self.AD_pn.add_place(it_p_age, 'p_age', 'Age risk factor', continuous = True)
        self.AD_pn.add_place(it_p_CD33, 'p_CD33', 'CD33 mutation', continuous = True) # 80 years old, risk factor in AD for BACE1 activity increase
    # 80 years old, risk factor in AD for BACE1 activity increase
    
        ##AB aggregation places
        self.AD_pn.add_place(it_p_Ab_S, place_id="p_Ab_S", label="Nucleated Ab", continuous = True)
        self.AD_pn.add_place(it_p_Ab_P, place_id="p_Ab_P", label="Ab oligomer", continuous = True)
        self.AD_pn.add_place(it_p_Ab_M, place_id="p_Ab_M", label="Ab fibril (mass)", continuous = True)
     # ER retraction and collapse
    
        # Monomeric RTN3 (cycling between axonal and perinuclear regions)
        self.AD_pn.add_place(it_p_RTN3_axon, place_id="p_RTN3_axon", label="Monomeric RTN3 (axonal)", continuous=True)
        self.AD_pn.add_place(it_p_RTN3_PN, place_id="p_RTN3_PN", label="Monomeric RTN3 (perinuclear)", continuous=True)
    
        # HMW RTN3 (cycling between different cellular compartments)
        self.AD_pn.add_place(it_p_RTN3_HMW_cyto, place_id="p_RTN3_HMW_cyto", label="HMW RTN3 (cytosol)", continuous=True)
        self.AD_pn.add_place(it_p_RTN3_HMW_auto, place_id="p_RTN3_HMW_auto", label="HMW RTN3 (autophagosome)", continuous=True)
        self.AD_pn.add_place(it_p_RTN3_HMW_lyso, place_id="p_RTN3_HMW_lyso", label="HMW RTN3 (degraded in lysosome)", continuous=True)
        self.AD_pn.add_place(it_p_RTN3_HMW_dys1, place_id="p_RTN3_HMW_dys1", label="HMW RTN3 (type I/III dystrophic neurites)", continuous=True)
        self.AD_pn.add_place(it_p_RTN3_HMW_dys2, place_id="p_RTN3_HMW_dys2", label="HMW RTN3 (type II dystrophic neurites)", continuous=True)
    
        # Energy metabolism: ATP consumption
        self.AD_pn.add_place(it_p_ATP, place_id="p_ATP", label="ATP", continuous=True)
        self.AD_pn.add_place(it_p_ADP, place_id="p_ADP", label="ADP", continuous=True)
        self.AD_pn.add_place(it_p_cas3, place_id="p_cas3", label="Active caspase 3", continuous=True)
        self.AD_pn.add_place(it_p_reduc_mito, place_id="p_reduc_mito", label="Reducing agents (mitochondria)", continuous=True)
        self.AD_pn.add_place(it_p_ROS_mito, place_id="p_ROS_mito", label="ROS (mitochondria)", continuous=True)
        self.AD_pn.add_place(it_p_H2O_mito, place_id="p_H2O_mito", label="H2O (mitochondria)", continuous=True)

        ##calcium
        
        self.AD_pn.add_place(it_p_Ca_cyto, "p_Ca_cyto", "Calcium (cytosol)", continuous = True)
        self.AD_pn.add_place(it_p_Ca_mito, "p_Ca_mito", "Calcium (mitochondria)", continuous = True)
        self.AD_pn.add_place(it_p_Ca_ER, "p_Ca_ER", "Calcium (ER)", continuous = True)
    
        # Discrete on/of-switches calcium pacemaking
        self.AD_pn.add_place(1, "p_Ca_extra", "on1 - Calcium (extracellular)", continuous = False)
        self.AD_pn.add_place(0, "p_on2","on2", continuous = False)
        self.AD_pn.add_place(0, "p_on3","on3", continuous = False)
        self.AD_pn.add_place(0, "p_on4","on4", continuous = False)
        

    def PD_Places(self):
        # Initialize an empty HFPN
        self.PD_pn = HFPN()
        
        #  # Cholesterol homeostasis
        self.PD_pn.add_place(PD_it_p_chol_PM, "p_chol_PM","Chol - perinuclear region", continuous = True)
        self.PD_pn.add_place(PD_it_p_chol_LE, "p_chol_LE", "Chol - late endosome", continuous = True)
        self.PD_pn.add_place(PD_it_p_chol_ER, "p_chol_ER", "Chol - ER", continuous = True)
        self.PD_pn.add_place(PD_it_p_chol_mito, "p_chol_mito", "Chol - mitochondria", continuous = True)
        self.PD_pn.add_place(PD_it_p_27OHchol_extra, "p_27OHchol_extra","27-OH chol - extracellular", continuous = True)
        self.PD_pn.add_place(PD_it_p_27OHchol_intra, "p_27OHchol_intra","27-OH chol - intracellular", continuous = True)
        self.PD_pn.add_place(PD_it_p_ApoEchol_extra, "p_ApoEchol_extra","ApoE - extracellular", continuous = True)
        self.PD_pn.add_place(PD_it_p_ApoEchol_EE, "p_ApoEchol_EE","ApoE - Early endosome", continuous = True)
        self.PD_pn.add_place(PD_it_p_7HOCA, "p_7HOCA","7-HOCA", continuous = True)
        self.PD_pn.add_place(PD_it_p_preg,place_id="p_preg", label="Pregnenolon", continuous=True)
        self.PD_pn.add_place(PD_it_p_24OHchol_extra,place_id="p_24OHchol_extra", label="24OHchol extra", continuous=True)
        self.PD_pn.add_place(PD_it_p_24OHchol_intra,place_id="p_24OHchol_intra", label="24OHchol intra", continuous=True)
    
        #  # PD specific places in cholesterol homeostasis
        self.PD_pn.add_place(PD_it_p_GBA1, "p_GBA1","GBA1", continuous = False)
        self.PD_pn.add_place(PD_it_p_SNCA_act_extra, "p_SNCA_act_extra","a-synuclein - extracellular", continuous = True)
        self.PD_pn.add_place(PD_it_p_SNCAApoEchol_extra, "p_SNCAApoEchol_extra","a-synuclein-ApoE complex - extracellular", continuous = True)
        self.PD_pn.add_place(PD_it_p_SNCAApoEchol_intra, "p_SNCAApoEchol_intra","a-synuclein-ApoE complex - intracellular", continuous = True)
    
        #  # Energy metabolism
        self.PD_pn.add_place(PD_it_p_ROS_mito, "p_ROS_mito", "ROS - mitochondria", continuous = True)
        self.PD_pn.add_place(PD_it_p_H2O_mito, "p_H2O_mito", "H2O - mitochondria", continuous = True)
        self.PD_pn.add_place(PD_it_p_reducing_agents, "p_reducing_agents", "Reducing agents - mitochondria", continuous = True)
        self.PD_pn.add_place(PD_it_p_cas3, "p_cas3","caspase 3 - mitochondria", continuous = True)
        self.PD_pn.add_place(PD_it_p_DJ1, "p_DJ1","DJ1 mutant", continuous = True)
        
        #  # Calcium homeostasis
        self.PD_pn.add_place(PD_it_p_Ca_cyto, "p_Ca_cyto", "Ca - cytosole", continuous = True)
        self.PD_pn.add_place(PD_it_p_Ca_mito, "p_Ca_mito","Ca - mitochondria", continuous = True)
        self.PD_pn.add_place(PD_it_p_Ca_ER, "p_Ca_ER", "Ca - ER", continuous = True)
        self.PD_pn.add_place(PD_it_p_ADP, "p_ADP","ADP - Calcium ER import", continuous = True)
        self.PD_pn.add_place(PD_it_p_ATP, "p_ATP","ATP - Calcium ER import", continuous = True)
    
        #  # Discrete on/of-switches calcium pacemaking
    
        self.PD_pn.add_place(1, "p_Ca_extra", "on1 - Ca - extracellular", continuous = False)
        self.PD_pn.add_place(0, "p_on2","on2", continuous = False)
        self.PD_pn.add_place(0, "p_on3","on3", continuous = False)
        self.PD_pn.add_place(0, "p_on4","on4", continuous = False)
        
          # Lewy bodies
        self.PD_pn.add_place(PD_it_p_SNCA_act, "p_SNCA_act","SNCA - active", continuous = True)
        self.PD_pn.add_place(PD_it_p_VPS35, "p_VPS35", "VPS35", continuous = True)
        self.PD_pn.add_place(PD_it_p_SNCA_inact, "p_SNCA_inact", "SNCA - inactive", continuous = True)
        self.PD_pn.add_place(PD_it_p_SNCA_olig, "p_SNCA_olig", "SNCA - Oligomerised", continuous = True)
        self.PD_pn.add_place(PD_it_p_LB, "p_LB", "Lewy body", continuous = True)
        self.PD_pn.add_place(PD_it_p_Fe2, "p_Fe2", "Fe2 iron pool", continuous = True)
        
          # Late endosome pathology 
        self.PD_pn.add_place(PD_it_p_LRRK2_mut, "p_LRRK2_mut","LRRK2 - mutated", continuous = True)
          # Monomeric RTN3 (cycling between axonal and perinuclear regions)
        self.PD_pn.add_place(PD_it_p_RTN3_axon, place_id="p_RTN3_axon", label="monomeric RTN3 (axonal)", continuous=True)
        self.PD_pn.add_place(PD_it_p_RTN3_PN, place_id="p_RTN3_PN", label="monomeric RTN3 (perinuclear)", continuous=True)
    
          # HMW RTN3 (cycling between different cellular compartments)
        self.PD_pn.add_place(PD_it_p_RTN3_HMW_cyto, place_id="p_RTN3_HMW_cyto", label="HMW RTN3 (cytosol)", continuous=True)
        self.PD_pn.add_place(PD_it_p_RTN3_HMW_auto, place_id="p_RTN3_HMW_auto", label="HMW RTN3 (autophagosome)", continuous=True)
        self.PD_pn.add_place(PD_it_p_RTN3_HMW_lyso, place_id="p_RTN3_HMW_lyso", label="HMW RTN3 (degraded in lysosome)", continuous=True)
        self.PD_pn.add_place(PD_it_p_RTN3_HMW_dys1, place_id="p_RTN3_HMW_dys1", label="HMW RTN3 (type I/III dystrophic neurites)", continuous=True)
        self.PD_pn.add_place(PD_it_p_RTN3_HMW_dys2, place_id="p_RTN3_HMW_dys2", label="HMW RTN3 (type II dystrophic neurites)", continuous=True)
    
          # Two places that are NOT part of this subpathway, but are temporarily added for establishing proper connections
          # They will be removed upon merging of subpathways
        self.PD_pn.add_place(PD_it_p_tau, place_id="p_tau", label = "Unphosphorylated tau", continuous = True)
        self.PD_pn.add_place(PD_it_p_tauP, place_id="p_tauP", label = "Phosphorylated tau", continuous = True)
        
        # Drug places 
        self.PD_pn.add_place(PD_it_p_NPT200, place_id="p_NPT200", label = "Drug NPT200", continuous = True)
        self.PD_pn.add_place(PD_it_p_DNL151, place_id="p_DNL151", label = "Drug DNL151", continuous = True)
        self.PD_pn.add_place(PD_it_p_LAMP2A, place_id="p_LAMP2A", label = "Drug LAMP2A", continuous = True)
               

    def PD_Continuous_Transitions(self):
        ## Define transitions
        
        # Cholesterol Endocytosis
        self.PD_pn.add_transition_with_speed_function( #1
                        transition_id                 = "t_LDLR_endocyto",
                        label                          = "LDLR endocyto",
                        input_place_ids                 = ["p_ApoEchol_extra", "p_chol_ER","p_LB"],
                        firing_condition             = PD_fc_t_LDLR_endocyto,
                        reaction_speed_function         = PD_r_t_LDLR_endocyto, 
                        consumption_coefficients     = [0,0,0],
                        output_place_ids             = ["p_ApoEchol_EE"],
                        production_coefficients         = [1],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = ["no","no"])
    
        # # Cleavage of cholesteryl esters
        self.PD_pn.add_transition_with_speed_function( #2
                        transition_id                 = "t_ApoEchol_cleav",
                        label                          = "ApoE-chol cleav",
                        input_place_ids                 = ["p_ApoEchol_EE"],
                        firing_condition             = PD_fc_t_ApoEchol_cleav,
                        reaction_speed_function         = PD_r_t_ApoEchol_cleav, 
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_chol_LE"],
                        production_coefficients         = [354],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = PD_collect_rate_analytics)
    
        # Transport Cholesterol from LE to ER
        self.PD_pn.add_transition_with_speed_function( #3
                        transition_id                 = "t_chol_trans_LE_ER",
                        label                          = "Chol transport LE-ER",
                        input_place_ids                 = ["p_chol_LE"],
                        firing_condition             = PD_fc_t_chol_trans_LE_ER,
                        reaction_speed_function         = PD_r_t_chol_trans_LE_ER,
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_chol_ER"],
                        production_coefficients         = [1],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = ["no","no"])
    
        # Transport Cholesterol from LE to mito
        self.PD_pn.add_transition_with_speed_function( #4
                        transition_id                 = "t_chol_trans_LE_mito",
                        label                          = "Chol transport LE-mito",
                        input_place_ids                 = ["p_chol_LE"],
                        firing_condition             = PD_fc_t_chol_trans_LE_mito,
                        reaction_speed_function         = PD_r_t_chol_trans_LE_mito,
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_chol_mito"],
                        production_coefficients         = [1],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = ["no","no"])
    
        # Transport Cholesterol from LE to PM
        self.PD_pn.add_transition_with_speed_function( #5
                        transition_id                 = "t_chol_trans_LE_PM",
                        label                          = "Chol transport LE-PM",
                        input_place_ids                 = ["p_chol_LE"],
                        firing_condition             = PD_fc_t_chol_trans_LE_PM, 
                        reaction_speed_function         = PD_r_t_chol_trans_LE_PM,
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_chol_PM"],
                        production_coefficients         = [1],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = ["no","no"])
    
        # Transport Cholesterol from PM to ER
        self.PD_pn.add_transition_with_speed_function( #6
                        transition_id                 = "t_chol_trans_PM_ER",
                        label                          = "Chol transport PM-ER",
                        input_place_ids                 = ["p_chol_PM"],
                        firing_condition             = PD_fc_t_chol_trans_PM_ER,
                        reaction_speed_function         = PD_r_t_chol_trans_PM_ER,
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_chol_ER"],
                        production_coefficients         = [1],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = PD_collect_rate_analytics)
    
        # Transport Cholesterol from ER to PM
        self.PD_pn.add_transition_with_speed_function( #7
                        transition_id                 = "t_chol_trans_ER_PM",
                        label                          = "Chol transport ER-PM",
                        input_place_ids                 = ["p_chol_ER"],
                        firing_condition             = PD_fc_t_chol_trans_ER_PM,
                        reaction_speed_function         = PD_r_t_chol_trans_ER_PM,
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_chol_PM"],
                        production_coefficients         = [1],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = ["no","no"])
    
        # Transport Cholesterol from ER to mito
        self.PD_pn.add_transition_with_speed_function( #8
                        transition_id                 = "t_chol_trans_ER_mito",
                        label                          = "Chol transport ER-mito",
                        input_place_ids                 = ["p_chol_ER"],
                        firing_condition             = PD_fc_t_chol_trans_ER_mito,
                        reaction_speed_function         = PD_r_t_chol_trans_ER_mito,
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_chol_mito"],
                        production_coefficients         = [1],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = ["no","no"])
    
        # Metabolisation of chol by CYP27A1
        self.PD_pn.add_transition_with_michaelis_menten( #9
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
                        collect_rate_analytics = ["no","no"])
    
        # Metabolism of chol by CYP11A1
        self.PD_pn.add_transition_with_michaelis_menten( #10
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
                        collect_rate_analytics = PD_collect_rate_analytics)
    
        # Metabolisation of 27OHchol by CYP7B1
        self.PD_pn.add_transition_with_michaelis_menten( #11
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
                        collect_rate_analytics = PD_collect_rate_analytics)
    
        # Endocytosis of 27OHchol
        self.PD_pn.add_transition_with_speed_function( #12
                        transition_id                 = "t_27OHchol_endocyto",
                        label                          = "27OHchol endocyto",
                        input_place_ids                 = ["p_27OHchol_extra"],
                        firing_condition             = PD_fc_t_27OHchol_endocyto,
                        reaction_speed_function         = PD_r_t_27OHchol_endocyto,
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_27OHchol_intra", "p_27OHchol_extra"],
                        production_coefficients         = [1,1],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = PD_collect_rate_analytics)
    
        # Metabolisation of chol by CYP46A1
        self.PD_pn.add_transition_with_michaelis_menten( #13
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
                        collect_rate_analytics = PD_collect_rate_analytics)
    
        # Exocytosis of 24OHchol
        self.PD_pn.add_transition_with_speed_function( #14
                        transition_id                 = "t_24OHchol_exocyto",
                        label                          = "24OHchol exocyto",
                        input_place_ids                 = ["p_24OHchol_intra"],
                        firing_condition             = PD_fc_t_24OHchol_exocyto,
                        reaction_speed_function         = PD_r_t_24OHchol_exocyto,
                        consumption_coefficients     = [1],
                        output_place_ids             = ["p_24OHchol_extra"],
                        production_coefficients         = [1],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = PD_collect_rate_analytics)
    
        # Transport of Chol into ECM
        self.PD_pn.add_transition_with_speed_function( #15
                        transition_id                 = "t_chol_trans_PM_ECM",
                        label                          = "Chol transport PM-ECM",
                        input_place_ids                 = ["p_chol_PM", "p_24OHchol_intra"],
                        firing_condition             = PD_fc_t_chol_trans_PM_ECM,
                        reaction_speed_function         = PD_r_t_chol_trans_PM_ECM,
                        consumption_coefficients     = [1,0],
                        output_place_ids             = [],
                        production_coefficients         = [],
                        stochastic_parameters = [cholSD],
                        collect_rate_analytics = ["yes", "no"])
    
    
        # PD specific
        #This transition is proven false, it should be removed.
        self.PD_pn.add_transition_with_speed_function( #16
                            transition_id = 't_SNCA_bind_ApoEchol_extra',
                            label = 'Extracellular binding of SNCA to chol',
                            input_place_ids = ['p_ApoEchol_extra','p_SNCA_act'],
                            firing_condition = PD_fc_t_SNCA_bind_ApoEchol_extra,
                            reaction_speed_function = PD_r_t_SNCA_bind_ApoEchol_extra,
                            consumption_coefficients = [0,30], 
                            output_place_ids = ['p_SNCA_olig'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = ["no","yes"])
    
        self.PD_pn.add_transition_with_speed_function( #17
                            transition_id = 't_chol_LE_upreg',
                            label = 'Upregulation of chol in LE',
                            input_place_ids = ['p_GBA1'],
                            firing_condition = PD_fc_t_chol_LE_upreg,
                            reaction_speed_function = PD_r_t_chol_LE_upreg,
                            consumption_coefficients = [0], # GBA1 is an enzyme
                            output_place_ids = ['p_chol_LE'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = PD_collect_rate_analytics)
        
        # # Calcium homeostasis
        
        self.PD_pn.add_transition_with_speed_function( #18
                            transition_id = 't_Ca_imp',
                            label = 'L-type Ca channel',
                            input_place_ids = ['p_Ca_extra'],
                            firing_condition = PD_fc_t_Ca_imp,
                            reaction_speed_function = PD_r_t_Ca_imp,
                            consumption_coefficients = [0], # Need to review this 
                            output_place_ids = ['p_Ca_cyto'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = ["no","yes"]) # Need to review this 
    
    
        self.PD_pn.add_transition_with_speed_function( #19
                            transition_id = 't_mCU',
                            label = 'Ca import into mitochondria via mCU',
                            input_place_ids = ['p_Ca_cyto','p_Ca_mito'],
                            firing_condition = PD_fc_t_mCU,
                            reaction_speed_function = PD_r_t_mCU,
                            consumption_coefficients = [1,0], 
                            output_place_ids = ['p_Ca_mito'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = ["no","yes"])
    
        self.PD_pn.add_transition_with_speed_function( #20
                            transition_id = 't_MAM',
                            label = 'Ca transport from ER to mitochondria',
                            input_place_ids = ['p_Ca_ER','p_Ca_mito'],
                            firing_condition = PD_fc_t_MAM,
                            reaction_speed_function = PD_r_t_MAM,
                            consumption_coefficients = [1,0], 
                            output_place_ids = ['p_Ca_mito'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = ["no","yes"])
    
        self.PD_pn.add_transition_with_speed_function( #21
                            transition_id = 't_RyR_IP3R',
                            label = 'Ca export from ER',
                            input_place_ids = ['p_Ca_extra','p_Ca_ER'],
                            firing_condition = PD_fc_t_RyR_IP3R,
                            reaction_speed_function = PD_r_t_RyR_IP3R,
                            consumption_coefficients = [0,1], 
                            output_place_ids = ['p_Ca_cyto'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = ["no","yes"]) 
    
        self.PD_pn.add_transition_with_speed_function( #22
                            transition_id = 't_SERCA',
                            label = 'Ca import to ER',
                            input_place_ids = ['p_Ca_cyto','p_ATP'],
                            firing_condition = PD_fc_t_SERCA,
                            reaction_speed_function = PD_r_t_SERCA,
                            consumption_coefficients = [1,1], #!!! Need to review this 0 should be 1
                            output_place_ids = ['p_Ca_ER','p_ADP'],         
                            production_coefficients = [1,1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = ["no","yes"]) # Need to review this
    
        self.PD_pn.add_transition_with_speed_function( #23
                            transition_id = 't_NCX_PMCA',
                            label = 'Ca efflux to extracellular space',
                            input_place_ids = ['p_Ca_cyto','p_on3'],
                            firing_condition = lambda a: a['p_on3']==1,
                            reaction_speed_function = PD_r_t_NCX_PMCA,
                            consumption_coefficients = [1,0], 
                            output_place_ids = [],         
                            production_coefficients = [],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = ["yes","no"])
        
        self.PD_pn.add_transition_with_speed_function( #24
                            transition_id = 't_mNCLX',
                            label = 'Ca export from mitochondria via mNCLX',
                            input_place_ids = ['p_Ca_mito','p_LRRK2_mut'],
                            firing_condition = PD_fc_t_mNCLX,
                            reaction_speed_function = PD_r_t_mNCLX,
                            consumption_coefficients = [1,0], 
                            output_place_ids = ['p_Ca_cyto'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = ["no","yes"]) 
    
        # # Discrete on/off-switches calcium pacemaking
    

        
        # Link to energy metabolism in that it needs ATP replenishment
        self.PD_pn.add_transition_with_mass_action( #29
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
        self.PD_pn.add_transition_with_speed_function( #30
                            transition_id = 't_SNCA_degr',
                            label = 'SNCA degradation by CMA',
                            input_place_ids = ['p_SNCA_act','p_VPS35','p_LRRK2_mut','p_27OHchol_intra','p_DJ1', 'p_DNL151', 'p_LAMP2A'],
                            firing_condition = PD_fc_t_SNCA_degr,
                            reaction_speed_function = PD_r_t_SNCA_degr,
                            consumption_coefficients = [1,0,0,0,0,0,0], 
                            output_place_ids = ['p_SNCA_inact'],         
                            production_coefficients = [1],
                            stochastic_parameters = [0],
                            collect_rate_analytics = dont_collect) 
    
        self.PD_pn.add_transition_with_speed_function(#31
                            transition_id = 't_SNCA_aggr',
                            label = 'SNCA aggregation',
                            input_place_ids = ['p_SNCA_act','p_Ca_cyto','p_ROS_mito', 'p_tauP', 'p_NPT200'],
                            firing_condition = PD_fc_t_SNCA_aggr,
                            reaction_speed_function = PD_r_t_SNCA_aggr,
                            consumption_coefficients = [30,0,0,0,0], #should be reviewed if Ca is consumed
                            output_place_ids = ['p_SNCA_olig'],         
                            production_coefficients = [1],
                            stochastic_parameters = [0],
                            collect_rate_analytics = dont_collect) 
    
        self.PD_pn.add_transition_with_speed_function(#32
                            transition_id = 't_SNCA_fibril',
                            label = 'SNCA fibrillation',
                            input_place_ids = ['p_SNCA_olig'],
                            firing_condition = PD_fc_t_SNCA_fibril,
                            reaction_speed_function = PD_r_t_SNCA_fibril,
                            consumption_coefficients = [100], 
                            output_place_ids = ['p_LB'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) 
    
        self.PD_pn.add_transition_with_speed_function(#33
                            transition_id = 't_IRE',
                            label = 'IRE',
                            input_place_ids = ['p_Fe2'],
                            firing_condition = PD_fc_t_IRE,
                            reaction_speed_function = PD_r_t_IRE,
                            consumption_coefficients = [0], 
                            output_place_ids = ['p_SNCA_act'],         
                            production_coefficients = [1],
                            stochastic_parameters = [0],
                            collect_rate_analytics = dont_collect) 
        
        # Energy metabolism
        self.PD_pn.add_transition_with_speed_function(#34
                            transition_id = 't_ATP_hydro_mito',
                            label = 'ATP hydrolysis in mitochondria',
                            input_place_ids = ['p_ATP'],
                            firing_condition = PD_fc_t_ATP_hydro_mito,
                            reaction_speed_function = PD_r_t_ATP_hydro_mito,
                            consumption_coefficients = [1], 
                            output_place_ids = ['p_ADP'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) 
        
        self.PD_pn.add_transition_with_speed_function(#35
                            transition_id = 't_ROS_metab',
                            label = 'ROS neutralisation',
                            input_place_ids = ['p_ROS_mito','p_chol_mito','p_LB','p_DJ1'],
                            firing_condition = PD_fc_t_ROS_metab,
                            reaction_speed_function = PD_r_t_ROS_metab,
                            consumption_coefficients = [1,0,0,0], 
                            output_place_ids = ['p_H2O_mito'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) 
        # #Link of krebs to calcium homeostasis
        self.PD_pn.add_transition_with_speed_function(#36
                            transition_id = 't_krebs',
                            label = 'Krebs cycle',
                            input_place_ids = ['p_ADP','p_Ca_mito'],
                            firing_condition = PD_fc_t_krebs,
                            reaction_speed_function = PD_r_t_krebs,
                            consumption_coefficients = [1,0], # Need to review this
                            output_place_ids = ['p_reducing_agents','p_ATP'],         
                            production_coefficients = [4,1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = PD_collect_rate_analytics) 
        
        #Link of ETC to calcium and cholesterol
        self.PD_pn.add_transition_with_speed_function(#37
                            transition_id = 't_ETC',
                            label = 'Electron transport chain',
                            input_place_ids = ['p_reducing_agents', 'p_ADP', 'p_Ca_mito', 'p_chol_mito','p_ROS_mito','p_LRRK2_mut'],
                            firing_condition = PD_fc_t_ETC,
                            reaction_speed_function = PD_r_t_ETC,
                            consumption_coefficients = [22/3,22,0,0,0,0], # Need to review this
                            output_place_ids = ['p_ATP', 'p_ROS_mito'],         
                            production_coefficients = [22,0.005],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = PD_collect_rate_analytics) 
    
        # # Output transitions: Cas3 for apoptosis
        self.PD_pn.add_transition_with_speed_function(#38
                            transition_id = 't_mito_dysfunc',
                            label = 'Mitochondrial complex 1 dysfunction',
                            input_place_ids = ['p_ROS_mito'],
                            firing_condition = PD_fc_t_mito_dysfunc,
                            reaction_speed_function = PD_r_t_mito_dysfunc,
                            consumption_coefficients = [1], 
                            output_place_ids = ['p_cas3'],         
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = PD_collect_rate_analytics) 
        
        self.PD_pn.add_transition_with_speed_function(#39
                            transition_id = 't_cas3_inact',
                            label = 'Caspase 3 degredation',
                            input_place_ids = ['p_cas3'],
                            firing_condition = PD_fc_t_cas3_inact,
                            reaction_speed_function = PD_r_t_cas3_inact,
                            consumption_coefficients = [1], # Need to review this
                            output_place_ids = [],         
                            production_coefficients = [],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) 
        
        # Late endosome pathology
        self.PD_pn.add_transition_with_michaelis_menten(#40
                            transition_id = 't_phos_tau',
                            label = 'Phosphorylation of tau',
                            Km = Km_t_phos_tau, 
                            vmax = kcat_t_phos_tau, 
                            input_place_ids = ['p_tau', 'p_SNCA_act'],
                            substrate_id = 'p_tau',
                            consumption_coefficients = [1, 0],
                            output_place_ids = ['p_tauP'],
                            production_coefficients = [1],
                            vmax_scaling_function = PD_vmax_scaling_t_phos_tau,
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) 
    
        self.PD_pn.add_transition_with_michaelis_menten(#41
                            transition_id = 't_dephos_tauP',
                            label = 'Dephosphorylation of tau protein',
                            Km = Km_t_dephos_tauP, 
                            vmax = vmax_t_dephos_tauP, 
                            input_place_ids = ['p_tauP', 'p_Ca_cyto'],
                            substrate_id = 'p_tauP',
                            consumption_coefficients = [1, 0],
                            output_place_ids = ['p_tau'],
                            production_coefficients = [1],
                            vmax_scaling_function = PD_vmax_scaling_t_dephos_tauP,
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) 
    
        self.PD_pn.add_transition_with_speed_function(#42
                            transition_id = 't_RTN3_exp',
                            label = 'Expression rate of RTN3',
                            input_place_ids = [], 
                            firing_condition = PD_fc_t_RTN3_exp,
                            reaction_speed_function = PD_r_t_RTN3_exp, 
                            consumption_coefficients = [],
                            output_place_ids = ['p_RTN3_PN'],
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) 
    
        self.PD_pn.add_transition_with_speed_function(#43
                            transition_id = 't_LE_retro',
                            label = 'retrograde transport of LEs & ER',
                            input_place_ids = ['p_ATP','p_chol_LE','p_RTN3_axon', 'p_tau','p_LRRK2_mut','p_LB'], 
                            firing_condition = PD_fc_t_LE_retro,
                            reaction_speed_function = PD_r_t_LE_retro, 
                            consumption_coefficients = [ATPcons_t_LE_trans, 0, 1, 0,0,0],
                            output_place_ids = ['p_ADP','p_RTN3_PN'],
                            production_coefficients = [ATPcons_t_LE_trans, 1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) 
    
        self.PD_pn.add_transition_with_speed_function(#44
                            transition_id = 't_LE_antero',
                            label = 'anterograde transport of LEs & ER',
                            input_place_ids = ['p_ATP','p_RTN3_PN', 'p_tau'], # didn't connect p_tau yet
                            firing_condition = PD_fc_t_LE_antero,
                            reaction_speed_function = PD_r_t_LE_antero, # get later from NPCD
                            consumption_coefficients = [ATPcons_t_LE_trans, 1, 0], # tune these coefficients based on PD
                            output_place_ids = ['p_ADP','p_RTN3_axon'],
                            production_coefficients = [ATPcons_t_LE_trans, 1],# tune these coefficients based on PD
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect)  
    
        self.PD_pn.add_transition_with_speed_function(#45
                            transition_id = 't_RTN3_aggregation',
                            label = 'aggregation of monomeric RTN3 into HMW RTN3',
                            input_place_ids = ['p_RTN3_axon', 'p_RTN3_PN'], 
                            firing_condition = PD_fc_t_RTN3_aggregation, # tune aggregation limit later
                            reaction_speed_function = PD_r_t_RTN3_aggregation,
                            consumption_coefficients = [1, 1],
                            output_place_ids = ['p_RTN3_HMW_cyto'],
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) 
    
        self.PD_pn.add_transition_with_speed_function(#46
                            transition_id = 't_RTN3_auto',
                            label = 'functional autophagy of HMW RTN3',
                            input_place_ids = ['p_RTN3_HMW_cyto', 'p_RTN3_axon'], 
                            firing_condition = PD_fc_t_RTN3_auto, 
                            reaction_speed_function = PD_r_t_RTN3_auto,
                            consumption_coefficients = [1, 0],
                            output_place_ids = ['p_RTN3_HMW_auto'],
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) 
    
        self.PD_pn.add_transition_with_speed_function(#47
                            transition_id = 't_RTN3_lyso',
                            label = 'functional delivery of HMW RTN3 to the lysosome',
                            input_place_ids = ['p_RTN3_HMW_auto', 'p_tau'], 
                            firing_condition = PD_fc_t_RTN3_lyso, 
                            reaction_speed_function = PD_r_t_RTN3_lyso,
                            consumption_coefficients = [1, 0],
                            output_place_ids = ['p_RTN3_HMW_lyso'],
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) 
    
        self.PD_pn.add_transition_with_speed_function(#48
                            transition_id = 't_RTN3_dys_auto',
                            label = 'dysfunctional autophagy of HMW RTN3',
                            input_place_ids = ['p_RTN3_HMW_cyto', 'p_RTN3_axon'], 
                            firing_condition = PD_fc_t_RTN3_dys_auto, 
                            reaction_speed_function = PD_r_t_RTN3_dys_auto,
                            consumption_coefficients = [1, 0],
                            output_place_ids = ['p_RTN3_HMW_dys1'],
                            production_coefficients = [1],# tune later when data are incorporated
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect)  
    
        self.PD_pn.add_transition_with_speed_function(#49
                            transition_id = 't_RTN3_dys_lyso',
                            label = 'dysfunctional delivery of HMW RTN3 to the lysosome',
                            input_place_ids = ['p_RTN3_HMW_auto', 'p_RTN3_HMW_dys1', 'p_tau'], 
                            firing_condition = PD_fc_t_RTN3_dys_lyso, 
                            reaction_speed_function = PD_r_t_RTN3_dys_lyso,
                            consumption_coefficients = [1, 0, 0],
                            output_place_ids = ['p_RTN3_HMW_dys2'],
                            production_coefficients = [1],# tune later when data are incorporated
                            stochastic_parameters = [SD],
                            collect_rate_analytics = dont_collect) 

        
    def PD_Discrete_Transitions(self):
        self.PD_pn.add_transition_with_speed_function( #25
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
        
        self.PD_pn.add_transition_with_speed_function( #26
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
        self.PD_pn.add_transition_with_speed_function( #27
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
        self.PD_pn.add_transition_with_speed_function( #28
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
        
        self.PD_pn.add_transition_with_speed_function(#50
                            transition_id = 't_MDV_Generation_basal',
                            label = "Mitochondrially Derived Vesicles production",
                            input_place_ids = ['p_chol_mito', 'p_ROS_mito'],
                            firing_condition = lambda a: a['p_chol_mito']>3.71e9,
                            reaction_speed_function = lambda a: 0.0011088*a['p_chol_mito']*(1/3500)*1, #This is a fraction of a single mitochondrion, and must divide by no. of mitochondria (1/3500)
                            consumption_coefficients =[0,0], #[1,0], turn on
                            output_place_ids = ['p_chol_LE'],
                            production_coefficients = [0],#[1], turn off
                            stochastic_parameters = [SD, cholSD],
                            collect_rate_analytics = ["no","no"],
                            delay = function_for_MDV_delay) #WARNING, DELAY IS CURRENTLY WRONG AND TOO SLOW, CHANGE TO 1/cholmp IN RATE FUNCTIONS
                            
        
        self.PD_pn.add_transition_with_speed_function(#51
                    transition_id = 't_Mitophagy',
                    label = "Mitochondria Cholesterol Transfer to Lysosomes",
                    input_place_ids = ['p_chol_mito'],
                    firing_condition = lambda a: a['p_chol_mito']>3.71e9,#Only fires if its higher than equilibrium value
                    reaction_speed_function = lambda a: (1/3500)*a['p_chol_mito']*1,
                    consumption_coefficients =[0], 
                    output_place_ids = ['p_chol_LE'],
                    production_coefficients = [0],
                    stochastic_parameters = [SD, cholSD],
                    collect_rate_analytics = ["no","no"],
                    delay = 310/chol_mp) #1 Mitophagy event every 310 seconds, (Arias-Fuenzalida et al., 2019). However, mitophagy increases due to other events, and this needs to be modelled in the future.
        
    def AD_parameters(self):
                # multiplicative rate factors for increasing rates of slow modules
        self.AD_Abeta_multiplier = 100
        tau_multiplier = 10
        chol_multiplier = 300
        ER_multiplier = 10
        # SD = 0.1
        # SDCalcium = 0.1
        
        neurone_cell_volume = 9008e-15 # L
        avagadros_constant = 6.022e23 # mol-1
        
        # Cholesterol homeostasis
        # downregulation via chol in ER, linear approximation y = m*x+n
        m_t_LDLR_endocyto = - 1.0682
        n_t_LDLR_endocyto = 2.0682
        
        fr_t_CYP46A1_metab = 0.08 # CYP46A1-accessible portion of ER cholesterol (to scale Km)
        Km_t_CYP46A1_metab = 5.70 * 10 ** 6 / fr_t_CYP46A1_metab
        vmax_t_CYP46A1_metab = 3.46 * 10 ** 3
        
        st_t_CYP27A1_metab = 0.13158 # CYP27A1-accessible portion of mitochondrial cholesterol (to scale Km)
        Km_t_CYP27A1_metab = 4.77 * 10 ** 7 / st_t_CYP27A1_metab
        vmax_t_CYP27A1_metab = 2.56 * 10 ** 3
        
        Km_t_CYP7B1_metab = 2.02 * 10 ** 7
        vmax_t_CYP7B1_metab = 4.32 * 10 ** 3
        
        st_t_CYP11A1_metab = 0.13158 # CYP11A1-accessible portion of mitochondrial cholesterol (to scale Km)
        Km_t_CYP11A1_metab = 7.59 * 10 ** 7 / st_t_CYP11A1_metab # CHANGED BASED ON SOURCE 2 DATA TO SEE IF IT'S BETTER
        vmax_t_CYP11A1_metab = 6.35 * 10 ** 4
        
        Km_t_ApoEchol_cleav = 1.39 * 10 ** 7
        vmax_t_ApoEchol_cleav = 1.86 * 10 ** 5
        
        Km_t_LDLR_endocyto = 1.30 * 10 ** 6
        vmax_t_LDLR_endocyto = 3.61633 * 10 ** 4
        
        k_t_EE_mat = 0.000924196 # s^-1
        
        k_t_chol_trans_LE_ER = 2.55357 * 10 ** (-4) # s^-1
        
        k_t_chol_trans_LE_mito = 2.36 * 10 ** (-6) # s^-1
        
        k_t_chol_trans_LE_PM = 0.002406761 # s^-1
        
        k_t_chol_trans_ER_PM = 1.725 * 10 ** (-3) # s^-1
        
        k_t_chol_trans_PM_ER = 1.56 * 10 ** (-6) # s^-1
        
        k_t_chol_trans_ER_mito = 1.1713 * 10 ** (-4) # s^-1
        
        k_t_27OHchol_endocyto = 2.65627 * 10 ** 2 # constant rate molecules/second, vary to represent different dietary cholesterol intakes
        
        k_t_chol_trans_PM_ECM = 8.2859 * 10 ** (-5) # s^-1
        
        # upregulation via 24-OHC, linear approximation y = m*x+n
        m_t_chol_trans_PM_ECM = 0.2356
        n_t_chol_trans_PM_ECM = 0.7644
        
        k_t_24OHchol_exocyto = 7.47488 * 10 ** (-6) # s^-1 
        
        disease_multiplier_27OH = 1 # set to true 
        
        
        # ER Retraction & Collapse
        
        beta_t_LE_retro = 1.667 #conversion factor of rate of retrograde transport to have it equal to anterograde transport in healthy cells 
        dist_t_LE_trans = 75e4 #distance in nm from perinuclear region to axon
        mchol_t_LE_retro = 2.27e-9 # scaling effect of cholesterol on retro transport
        nchol_t_LE_retro = 1 - mchol_t_LE_retro * it_p_chol_LE # scaling effect of cholesterol on retro transport
        vmax_t_LE_retro = 892 #Vmax in nm/s
        Km_t_LE_retro = 3510864000 #K_M in particles of ATP
        vmax_t_LE_antero = 814 #Vmax in nm/s
        Km_t_LE_antero = 614040000 #K_M in particles of ATP
        ATPcons_t_LE_trans = 0 # dist_t_LE_trans / 8 # each step of the motor consumes 1 ATP & travels 8 nm; total ATP consumed = number of steps
        
        k_t_RTN3_exp = 113.3
        Ab_t_RTN3_aggregation = 641020
        dec_t_RTN3_aggregation = 0.762
        
        k_t_RTN3_auto = 0.011111111
        
        k_t_RTN3_lyso = 0.000826667
        
        mitprop_t_RTN3_dys_auto = 0.885
        
        
        # Abeta Pathology
        k_t_asec_exp = 96.8
        mchol_t_asec_exp = 7.19184e-9
        nchol_t_asec_exp = -1.86
        k_t_asec_degr = 1.60e-5
        
        k_t_APP_endocyto = 9.67e-5
        dis_t_APP_endocyto = 0.0832033 # Compatible with the ApoE4 0/1 input representing 0 alleles & 2 alleles
        k_t_APP_exp = 45000 
        dis_t_APP_exp = 0.25 # representing Apoe4 contribution to parameter change
        m_t_APP_exp = 0.5/(693.444*it_p_ROS_mito)
        n_t_APP_exp = 1 - it_p_ROS_mito * m_t_APP_exp
        k_t_APP_endo_event = .0001435 
        
        k_t_bsec_exp = 11.138 
        mchol_t_bsec_exp = 1.52842e-8
        nchol_t_bsec_exp = 0.532332
        nRTN_t_bsec_exp = 1.78571
        mRTN_t_bsec_exp = -(nRTN_t_bsec_exp-1)/it_p_RTN3_axon
        mROS_t_bsec_exp = .5/it_p_ROS_mito
        nROS_t_bsec_exp = 0.5
        k_t_bsec_degr = 1.655e-5
        mchol_t_APP_bsec_cleav = 8.13035e-12
        nchol_t_APP_bsec_cleav = 0.312985106
        age_t_APP_bsec_cleav = 0.44
        
        k_t_gsec_exp = 53.92 
        k_t_gsec_degr = 1.6e-5 # assume same as asec and bsec for now - may update later
        
        k_t_Ab_degr = 0.00188
        
        Km_t_APP_asec_cleav = 19034084
        kcat_t_APP_asec_cleav = 0.0474783
        
        Km_t_APP_bsec_cleav = 37972323
        kcat_t_APP_bsec_cleav = 0.002
        
        Km_t_CTF99_gsec_cleav = 169223
        kcat_t_CTF99_gsec_cleav = 0.00167
        
        
        Km_t_Ab_elon = 17343360
        Vmax_t_Ab_elon = 1.108
        
        # Tau Pathology
        k_t_actv_GSK3b = 8.33e-3
        m_t_act_GSK3b = 4.07e-7 # TODO: tune this, increase m to increase effect
        n_t_act_GSK3b = 1 - m_t_act_GSK3b * it_p_Ab
        dis_t_act_GSK3b = 0.433
        
        k_t_inactv_GSK3b = 7.95e-3
        
        Km_t_phos_tau = 9.22e7
        kcat_t_phos_tau = 0.146464095 
        
        Km_t_dephos_tauP = 6.29e7
        vmax_t_dephos_tauP = 1.17*1.1e6  # uM/min/ 20 units per mL PP-2A, TODO: conevert unit
        
        k_t_p_GSK3b_deg = 100*1.6e-5 #  (standard protein degradation rate)
        k_t_p_GSK3b_exp = k_t_p_GSK3b_deg * it_p_GSK3b_inact
        
        
        # Calcium Homeostasis
        k_t_NCX_PMCA = 10 #multiplied by 10 compared to Gabi's paper (Gabriel, 2020)
        k_t_NaK_ATPase= 0.70 
        k_t_mCU1=(1*1e6)/(17854326) #rate mCU /average Ca_cyto in homeostasis
        k_t_mCU2=(5000)/(17854326) #rate mCU /average Ca_cyto in homeostasis
        #k_t_mNCLX=(5000)/(3.6*1e7) #rate mCU /average Ca_cyto in homeostasis
        k_t_mNCLX=0.066666667
        k_t_MAM=1e6/1.8e9 #rate MAM
        k_t_SERCA_no_ATP=0.05638 #(1e6+100)/17854326#0.05638 #100/1785#4#3#2#6#/(5.407*1e9)
        k_t_SERCA_ATP=k_t_SERCA_no_ATP/5.42e9 #rate mCU /average ATP in homeostasis
        k_t_RyR_IP3R = 100/(1.8*1e9) #rate mCU /average Ca_ER in homeostasis
        
        
        # Energy metabolism
        k_t_krebs = (1.63*10**(-7))*2968656.262/3e7 
        k_t_ATP_hydro_mito = 1.92*10**(-2)
        k_t_ETC = 2.48*10**(-5)*2968656.262/3e7 
        m_t_ETC_inhib_Ab = -1.6438e-6 # -7.5786*10**(-7)
        n_t_ETC_inhib_Ab = 1.0559681024 #1 - m_t_ETC_inhib_Ab * it_p_Ab
        k_t_ROS_metab = 5.875*10**10
        k_t_mito_dysfunc = 1.0495e2 # s^-1 For time step of 0.01 s, change to 1.037984e2
        m_t_mito_dysfunc = 3.1855e-5
        n_t_mito_dysfunc = 0.61
        m_t_mito_dysfunc_Ab = 1.27 * 10 ** (-7)
        n_t_mito_dysfunc_Ab = 0.9957
        k_t_cas3_inact = 7.96721 * 10 ** (-3) # s^-1
        k_t_ROS_gener_Ab = 8.4e-1 # s^-1  maximum is 7e3
    def AD_Continuous_Transitions(self):
        
        
        ## Transitions
        # Cholesterol Endocytosis
        self.AD_pn.add_transition_with_speed_function(
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
        self.AD_pn.add_transition_with_speed_function(
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
    
    #     # Transport Cholesterol from LE to mito
        self.AD_pn.add_transition_with_speed_function(
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
        self.AD_pn.add_transition_with_speed_function(
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
        self.AD_pn.add_transition_with_speed_function(
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
        self.AD_pn.add_transition_with_speed_function(
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
        self.AD_pn.add_transition_with_speed_function(
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
        self.AD_pn.add_transition_with_michaelis_menten(
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
        self.AD_pn.add_transition_with_michaelis_menten(
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
        self.AD_pn.add_transition_with_michaelis_menten(
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
        self.AD_pn.add_transition_with_speed_function(
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
        self.AD_pn.add_transition_with_michaelis_menten(
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
        self.AD_pn.add_transition_with_speed_function(
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
        self.AD_pn.add_transition_with_speed_function(
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
        self.AD_pn.add_transition_with_speed_function(
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
    
        self.AD_pn.add_transition_with_speed_function(
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
    
    
        self.AD_pn.add_transition_with_speed_function(
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
            

        self.AD_pn.add_transition_with_michaelis_menten(
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
    
    
        self.AD_pn.add_transition_with_michaelis_menten(
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
        self.AD_pn.add_transition_with_michaelis_menten(
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
    
        self.AD_pn.add_transition_with_speed_function(
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
        
        self.AD_pn.add_transition_with_speed_function(
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
    
        self.AD_pn.add_transition_with_speed_function(
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
    
        self.AD_pn.add_transition_with_speed_function(
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
        
        self.AD_pn.add_transition_with_speed_function(
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
    
        self.AD_pn.add_transition_with_michaelis_menten(
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
    
        self.AD_pn.add_transition_with_speed_function(
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
        
        self.AD_pn.add_transition_with_speed_function(
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
    
        self.AD_pn.add_transition_with_michaelis_menten(
                        transition_id                 = 't_CTF99_gsec_cleav',
                        label                         = 'Gamma secretase cleavage of CTF99',
                        Km = Km_t_CTF99_gsec_cleav, 
                        vmax = kcat_t_CTF99_gsec_cleav,
                        input_place_ids                 = ['p_CTF99', 'p_gsec', 'p_chol_PM'],
                        substrate_id = 'p_CTF99', 
                        consumption_coefficients     = [1, 0, 0],
                        output_place_ids = ['p_Abconc', 'p_Ab', 'p_AICD'],
                        production_coefficients = [conversion, 1, 1],
                        vmax_scaling_function = vmax_scaling_t_CTF99_gsec_cleav,
                        stochastic_parameters = [SD],
                        collect_rate_analytics = collect_rate_analytics)
    
        self.AD_pn.add_transition_with_speed_function(
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
        
        self.AD_pn.add_transition_with_speed_function(
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
    
        self.AD_pn.add_transition_with_speed_function(
                        transition_id                 = 't_Ab_degr',
                        label                         = 'Ab degradation',
                        input_place_ids                 = ['p_Ab', 'p_Abconc'], 
                        firing_condition             = fc_t_Ab_degr,
                        reaction_speed_function         = r_t_Ab_degr,
                        consumption_coefficients     = [1, conversion], 
                        output_place_ids = [],
                        production_coefficients = [],
                        stochastic_parameters = [SD],
                        collect_rate_analytics = collect_rate_analytics)# TODO - fix ratio


    
    #AB aggregation module
      #AB Aggregation transitions
            
        self.AD_pn.add_transition_with_speed_function(transition_id = 't_Ab_nuc1',
                            label                = "Ab primary nucleation",
                            input_place_ids       = ['p_Ab', 'p_Abconc'],
                            firing_condition = fc_t_Ab_nuc1,
                            reaction_speed_function = r_t_Ab_nuc1,
                            consumption_coefficients  = [1/conversion, 1], 
                            output_place_ids       = ['p_Ab_S'],
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)

        
        self.AD_pn.add_transition_with_speed_function(transition_id = 't_Ab_dis1',
                            label                = "Ab dissociation1",
                            input_place_ids       = ['p_Ab_S'],
                            firing_condition = fc_t_Ab_dis1,
                            reaction_speed_function = r_t_Ab_dis1,
                            consumption_coefficients  = [1], 
                            output_place_ids       = ['p_Ab', 'p_Abconc'],
                            production_coefficients = [1/conversion, 1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
    
        self.AD_pn.add_transition_with_speed_function(transition_id = 't_Ab_elon',
                            label                = "Ab elongation",
                            input_place_ids       = ['p_Ab_S'],
                            firing_condition = fc_t_Ab_elon,
                            reaction_speed_function = r_t_Ab_elon,
                            consumption_coefficients  = [1], 
                            output_place_ids       = ['p_Ab_P'],
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
        
        self.AD_pn.add_transition_with_speed_function(transition_id = 't_Ab_fib',
                            label                = "Ab fibrillation",
                            input_place_ids       = ['p_Ab_P', 'p_Ab', 'p_Abconc'],
                            firing_condition = fc_t_Ab_fib,
                            reaction_speed_function = r_t_Ab_fib,
                            consumption_coefficients  = [0, 0, 0],
                            output_place_ids       = ['p_Ab_M'],
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
    
        self.AD_pn.add_transition_with_speed_function(transition_id = 't_Ab_M_frag',
                            label                = "Ab fibril fragmentation",
                            input_place_ids       = ['p_Ab_M'],
                            firing_condition = fc_t_Ab_M_frag,
                            reaction_speed_function = r_t_Ab_M_frag,
                            consumption_coefficients  = [1], 
                            output_place_ids       = ['p_Ab_P'],
                            production_coefficients = [1],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
            
        self.AD_pn.add_transition_with_speed_function(transition_id = 't_Ab_M_phag',
                            label                = "Ab fibril phagocytosis",
                            input_place_ids       = ['p_Ab_P', 'p_age', 'p_CD33'],
                            firing_condition = fc_t_Ab_P_phag,
                            reaction_speed_function = r_t_Ab_P_phag,
                            consumption_coefficients  = [1, 0, 0], 
                            output_place_ids       = [],
                            production_coefficients = [],
                            stochastic_parameters = [SD],
                            collect_rate_analytics = collect_rate_analytics)
            
        
    
        self.AD_pn.add_transition_with_speed_function(
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
        
        self.AD_pn.add_transition_with_speed_function(
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
    
        self.AD_pn.add_transition_with_speed_function(
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
    
        self.AD_pn.add_transition_with_speed_function(
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
    
        self.AD_pn.add_transition_with_speed_function(
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
    
        self.AD_pn.add_transition_with_speed_function(
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
    
        self.AD_pn.add_transition_with_speed_function(
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
    
        self.AD_pn.add_transition_with_speed_function(
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
        self.AD_pn.add_transition_with_speed_function(  
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
        
        self.AD_pn.add_transition_with_speed_function(  
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
        
        self.AD_pn.add_transition_with_speed_function(  
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
        
        self.AD_pn.add_transition_with_speed_function(  
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
        self.AD_pn.add_transition_with_speed_function(
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
        self.AD_pn.add_transition_with_speed_function(
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
        
        self.AD_pn.add_transition_with_speed_function(
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
        self.AD_pn.add_transition_with_speed_function(
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
    
        self.AD_pn.add_transition_with_speed_function(
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
    
        self.AD_pn.add_transition_with_speed_function(
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
                            
    
        self.AD_pn.add_transition_with_speed_function(
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
    
        self.AD_pn.add_transition_with_speed_function(
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
    
        self.AD_pn.add_transition_with_speed_function(
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
        
        self.AD_pn.add_transition_with_speed_function(
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
    

    
        # Link to energy metabolism in that it needs ATP replenishment
        self.AD_pn.add_transition_with_mass_action(
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

        
        
    def AD_Discrete_Transitions(self):
        
        # # Discrete on/of-switches calcium pacemaking
        self.AD_pn.add_transition_with_speed_function(
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
        
        self.AD_pn.add_transition_with_speed_function(
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
        
        self.AD_pn.add_transition_with_speed_function(
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
        
        self.AD_pn.add_transition_with_speed_function(
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
        


 
        self.AD_pn.add_transition_with_speed_function(
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
        
        
    # def make_scrollbar_AD_sHFPN(self): #might be redundant
    #     self.AD_canvas = tk.Canvas(self.AD_frame1)
    #     self.AD_canvas.pack(side="left", fill=tk.BOTH, expand=1)
        
    #     self.AD_scrollbar = ttk.Scrollbar(self.AD_frame1, orient=tk.VERTICAL, command =self.canvas.yview)
    #     self.AD_scrollbar.pack(side="left", fill=tk.Y)
        
    #     self.AD_canvas.configure(yscrollcommand=self.AD_scrollbar.set)
    #     self.AD_canvas.bind('<Configure>', lambda e: self.AD_canvas.configure(scrollregion= self.AD_canvas.bbox("all")))
        
    #     #Create another frame inside the canvas
    #     self.AD_frame_in_canvas = tk.Frame(self.AD_canvas)
    #     self.AD_canvas.create_window((0,0), window=self.AD_frame_in_canvas, anchor="nw")
        
        
    def make_scrollbar_Analysis(self):
        self.canvas2 = tk.Canvas(self.frame5)

        
        self.scrollbar2 = ttk.Scrollbar(self.frame5, orient=tk.VERTICAL, command =self.canvas2.yview)
        self.scrollbar2.pack(side="right", fill=tk.Y)

        self.scrollbarhori = ttk.Scrollbar(self.frame5, orient=tk.HORIZONTAL, command =self.canvas2.xview)
        self.scrollbarhori.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.canvas2.configure(yscrollcommand=self.scrollbar2.set, xscrollcommand=self.scrollbarhori.set)
        self.canvas2.bind('<Configure>', lambda e: self.canvas2.configure(scrollregion= self.canvas2.bbox("all")))      
        self.canvas2.pack(side="left", fill=tk.BOTH, expand=1)
        #Create another frame inside the canvas2
        self.frame_in_canvas_Analysis = tk.Frame(self.canvas2)
        self.canvas2.create_window((0,0), window=self.frame_in_canvas_Analysis, anchor="nw") 
        self.frame_in_canvas_Analysis.config(background="grey42")
        
        
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
        self.AD_Label_run_save_name = tk.Label(self.AD_frame3_in_canvas_Inputs, text="Run Save Name")
        self.AD_Label_run_save_name.grid(row=0,column=0)
        self.AD_Label_run_save_name_e = tk.Entry(self.AD_frame3_in_canvas_Inputs)
        self.AD_Label_run_save_name_e.grid(row=0,column=1)
        self.AD_Label_run_save_name_e.insert(tk.END, "sHFPN_Save_Name")
        #*Number of Timesteps*
        self.AD_Label_no_timesteps = tk.Label(self.AD_frame3_in_canvas_Inputs, text="Number of Timesteps")
        self.AD_Label_no_timesteps.grid(row=1,column=0)
        self.AD_Label_no_timesteps_e = tk.Entry(self.AD_frame3_in_canvas_Inputs)
        self.AD_Label_no_timesteps_e.grid(row=1,column=1)

        self.AD_Label_no_timesteps_e.insert(tk.END, "100")
        self.AD_Label_Help_no_timesteps = tk.Label(self.frame_in_canvas_Inputs, text="Only input increments of 1000")

        self.AD_Label_Help_no_timesteps.grid(row=1, column=2)
        #*Timestep Size*
        self.AD_Label_timestep_size = tk.Label(self.AD_frame3_in_canvas_Inputs, text="Timestep Size (s)")
        self.AD_Label_timestep_size.grid(row=2,column=0)
        self.AD_Label_timestep_size_e = tk.Entry(self.AD_frame3_in_canvas_Inputs)
        self.AD_Label_timestep_size_e.grid(row=2,column=1)
        self.AD_Label_timestep_size_e.insert(tk.END, "0.001")
         
        
        #*Mutations Header*
        Mutations_Header = tkfont.Font(family='Helvetica', size=10, weight="bold", slant="italic") 
        self.Label_Header_Mutations = tk.Label(self.AD_frame3_in_canvas_Inputs, text="Mutations and Risk Factors", font= Mutations_Header)
        self.Label_Header_Mutations.grid(row=6, column=1)
        
        #*ApoE4 Mutation
        self.AD_ApoE4_Mutation = tk.Label(self.AD_frame3_in_canvas_Inputs, text="ApoE4")
        self.AD_ApoE4_Mutation.grid(row=7, column=0)
        self.AD_ApoE4_var = tk.IntVar()
        self.AD_ApoE4_Mutation_checkbox = tk.Checkbutton(self.AD_frame3_in_canvas_Inputs, variable=self.AD_ApoE4_var)
        self.AD_ApoE4_Mutation_checkbox.grid(row=7, column=1)

        #CD33 mutation
        self.AD_CD33_Mutation = tk.Label(self.AD_frame3_in_canvas_Inputs, text="CD33")
        self.AD_CD33_Mutation.grid(row=8, column=0)
        self.AD_CD33_var = tk.IntVar()
        self.AD_CD33_Mutation_checkbox = tk.Checkbutton(self.AD_frame3_in_canvas_Inputs, variable=self.AD_CD33_var)
        self.AD_CD33_Mutation_checkbox.grid(row=8, column=1)
            
         #Aged 
        self.AD_Aged_risk = tk.Label(self.AD_frame3_in_canvas_Inputs, text="Aged")
        self.AD_Aged_risk.grid(row=9, column=0)
        self.AD_Aged_var = tk.IntVar()
        self.AD_Aged_risk_checkbox = tk.Checkbutton(self.AD_frame3_in_canvas_Inputs, variable=self.AD_Aged_var)
        self.AD_Aged_risk_checkbox.grid(row=9, column=1)
                       
        
        
        def AD_save_entry_inputs(self):
            self.AD_HFPN_run_save_name =self.AD_Label_run_save_name_e.get()
            self.AD_HFPN_number_of_timesteps = self.AD_Label_no_timesteps_e.get()
            self.AD_HFPN_timestep_size = self.AD_Label_timestep_size_e.get()
            # self.AD_HFPN_CholSD = self.AD_Label_CholSD_e.get()
            # self.AD_HFPN_CalciumSD = self.AD_Label_Calcium_e.get()
            print("Inputs Saved")
            self.AD_button_1.config(state="normal", text="Run sHFPN")
            self.AD_button_1.config(state="normal", text="Run AD sHFPN")            
            self.AD_button_6.config(state=tk.DISABLED)
            
        #*Save Inputs Button*
        self.AD_button_6 = tk.Button(self.AD_frame3_in_canvas_Inputs, text = "Save Inputs", cursor="hand2", command=partial(AD_save_entry_inputs, self))    
        self.AD_button_6.grid(row=20, column=1, pady=20)  
        self.AD_Label_Save_Inputs_Button_info = tk.Label(self.AD_frame3_in_canvas_Inputs, text="Double check your inputs")
        self.AD_Label_Save_Inputs_Button_info.grid(row=20, column=2)        
        
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
        self.Label_no_timesteps_e.insert(tk.END, "6000000")
        self.Label_Help_no_timesteps = tk.Label(self.frame_in_canvas_Inputs, text="Only input increments of 1000")
        self.Label_Help_no_timesteps.grid(row=1, column=2)
        #*Timestep Size*
        self.Label_timestep_size = tk.Label(self.frame_in_canvas_Inputs, text="Timestep Size (s)")
        self.Label_timestep_size.grid(row=2,column=0)
        self.Label_timestep_size_e = tk.Entry(self.frame_in_canvas_Inputs)
        self.Label_timestep_size_e.grid(row=2,column=1)
        self.Label_timestep_size_e.insert(tk.END, "0.001")
        
        #*SD Header*
        SD_font = tkfont.Font(family='Helvetica', size=10, weight="bold", slant="italic")
        self.Label_Header = tk.Label(self.frame_in_canvas_Inputs, text="Adjust Transition Stochasticity Levels", font=SD_font)
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
            self.lb.itemconfig(7, bg="red")
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
        self.Label_BSL = tk.Label(self.frame7, text="Please email B.S. Lockey at brandonlockey@icloud.com for issues.", font=self.BSL_font)
        self.Label_BSL.pack()

    def Live_Graph(self):
        self.frame8=tk.Frame(self.frame2)
        self.frame8.grid(row=0, column=0, sticky="nsew")
        
        #Label
        # self.Label_Neuronal_Healthbar = tk.Label(self.frame8, text="Under Construction...")
        # self.Label_Neuronal_Healthbar.pack()
        
        #Embedded Graphs (PROBABLY HAVE TO APPEND THIS TO SELF LATER, SO CAN BE ACCESSED)

        # self.f = Figure(figsize=(5,5), dpi=100)
        # self.a = self.f.add_subplot(111)
        # self.a.plot([1,2,3,4,5,6,7,8],[1,2,3,4,5,6,7,8])
        # self.Neuronal_Healthbar_canvas = FigureCanvasTkAgg(self.f, self.frame8)
        # self.Neuronal_Healthbar_canvas.draw()
        # self.Neuronal_Healthbar_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)#I can also choose to grid it so its more compact for later, when I want to plot multiple plots. 
        # toolbar = NavigationToolbar2Tk(self.Neuronal_Healthbar_canvas, self.frame8)
        # toolbar.update()
        # self.Neuronal_Healthbar_canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        
        
    def Run_sHFPN_Page(self):
        #PD Button
        self.frame4=tk.Frame(self.frame2)
        self.frame4.grid(row=0,column=0,sticky="nsew")
        self.button_1 = tk.Button(self.frame4, text="Save PD Inputs", state=tk.DISABLED, command= threading.Thread(target = partial(self.run_sHFPN)).start)
        self.button_1.config(cursor="hand2")
        self.button_1.pack(side=tk.TOP)
        #AD Button
        self.AD_button_1 = tk.Button(self.frame4, text="Save AD Inputs", state=tk.DISABLED, command= threading.Thread(target = partial(self.run_AD_sHFPN)).start)
        self.AD_button_1.config(cursor="hand2")
        self.AD_button_1.pack(side=tk.TOP)        

        self.make_scrollbar_sHFPN()
        
    def Analysis_page(self):
        self.frame5=tk.Frame(self.frame2)
        #self.frame5.pack(side="left", fill=tk.BOTH,expand=1)
        self.frame5.grid(row=0,column=0,sticky="nsew")
        self.frame5.config(bg="grey42")
        self.run_save_name_entry = tk.Entry(self.frame5, width=50, bg="black", fg="violet", borderwidth="5")
        self.run_save_name_entry.pack()
        
        def insert_run_name(self):
            self.run_save_name_entry.delete(0, tk.END)
            self.run_save_name_entry.insert(tk.END, self.saved_run_string)
        def Go_to_saved_runs(self):
            self.frame6.destroy()
            self.show_saved_runs()
            self.frame6.tkraise()
            self.button_saved_run.config(text="Input Last Hovered Saved Run",state=tk.DISABLED, command=partial(insert_run_name, self))
        
        
        self.button_saved_run = tk.Button(self.frame5, text="Go To Saved Runs", command=partial(Go_to_saved_runs, self))
        self.button_saved_run.pack()
        
        
        def save_entry(self):
            "saves run_save_name entry"
            if self.run_save_name_entry.get() =="":
                self.run_save_name_entry.config(bg="red")
            else:
                self.run_save_name =self.run_save_name_entry.get()
                self.button_2.config(state="normal", text="Run Analysis")
                print(self.run_save_name)
                self.button3.config(state=tk.DISABLED)
                self.run_save_name_entry.config(bg="black")
                self.button_saved_run.config(state=tk.DISABLED)
            
        self.button3 = tk.Button(self.frame5, text="Enter run_save_name", command = partial(save_entry, self))
        self.button3.config(cursor="hand2")
        self.button3.pack()
        

            
        
        def GUI_plot(place_id, analysis, File, simulation_time_step, desired_plotting_steps, max_time_step):  
            place_label =""
            plot_title = place_id
            desired_plotting_steps = int(self.desired_plotting_steps_entry_box.get())
           
            if desired_plotting_steps>max_time_step: #in case user inputs more timesteps than available
                desired_plotting_steps = max_time_step
            if desired_plotting_steps %2==0: #if even, subtract 1, avoid errors.(only works if odd for some reason)
                desired_plotting_steps = desired_plotting_steps-1
                
                
            t=np.arange(0,desired_plotting_steps*simulation_time_step+simulation_time_step,simulation_time_step) #(start,end,step) end in seconds. end = 1000 with ts=0.001 means you have 1000000 datapoints.

            t=t[0::int(self.nth_datapoint_entry_box.get())] #takes every nth data point. But still need to make sure the Axes are right somehow.                
          
            #truncate t by 1
          
            fig,ax=plt.subplots()
            
            data = self.analysis[File].mean_token_history_for_places([place_id])[0:desired_plotting_steps+1] 
            data = data[0::int(self.nth_datapoint_entry_box.get())]
            if self.Analysis_print_mean_value_var:
                print("Mean: ", np.mean(data))        
            option2 = self.Analysis_plot_rolling_only_var.get()
            if option2==0:
                if place_label == "":
                    ax.plot(t, data, label = File,  color="black")
                else:
                    ax.plot(t, data, label = File+' - '+place_label, color="black")  
                
            self.Analysis_rolling_average_decision=self.Analysis_rolling_average.get()
            da_window_size = int(self.Analysis_RAWS_entry.get())            
            if self.Analysis_rolling_average_decision ==1:
                data2 = data.ravel()
                data2 = np.convolve(data2, np.ones(da_window_size), "valid")/da_window_size
                an_array = np.empty(da_window_size-1)
                an_array[:] = np.NaN
                data2 = np.insert(data2, 0, an_array)
                plt.plot(t, data2, color="red")         
           
            Analysis.standardise_plot(ax, title = plot_title, xlabel = "Time (s)",ylabel = "Molecule count")

            if self.Analysis_y_threshold_entry.get() != "":
                plt.axhline(y=float(self.Analysis_y_threshold_entry.get()), linestyle='--', color ='red', label = self.Analysis_y_threshold_graph_label.get())      
       
            if self.Analysis_plotting_text_list_entry.get() == "":
                ax.legend()
            else:
                L = ax.legend()
                L.get_texts()[0].set_text(self.Analysis_plotting_text_list_entry.get())                        
            
            if self.Analysis_x_lim_entry.get() != "":
                split_list = self.Analysis_x_lim_entry.get().split(", ")
                x_lim_0 = float(split_list[0])
                x_lim_1 = float(split_list[1])
                plt.xlim([x_lim_0,x_lim_1])
                
            if self.Analysis_y_lim_entry.get() != "":
                split_list = self.Analysis_y_lim_entry.get().split(", ")
                y_lim_0 = float(split_list[0])
                y_lim_1 = float(split_list[1])
                plt.ylim([y_lim_0,y_lim_1])
                
            if self.Analysis_Plot_Title.get() != "":
                plt.title(self.Analysis_Plot_Title.get())
                
            if self.Analysis_Plot_Y_Axis_Label_Entry.get() != "":
                plt.ylabel(self.Analysis_Plot_Y_Axis_Label_Entry.get())
            
            plt.show()
            
            
            if self.Export_var.get() ==1:
                thename = "../saved-csvs/"+str(self.CSV_save_name.get())+".csv"
                with open(thename, 'w', newline='') as csvfile:
                    token_header = place_id+' Tokens'
                    fieldnames = ['Time (s)', token_header]
                    thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    thewriter.writeheader()
                    for thetime, token in zip(t,data):
                        thewriter.writerow({'Time (s)':thetime, token_header:token[0]})
                print("CSV Saved at " + thename)
            self.csv_listbox.destroy()
            self.csv_list_box_function() 
            self.update_truth_list()
        def GUI_Plot_Rate(col, analysis, File, simulation_time_step, desired_plotting_steps, max_time_step, CONS_OR_PROD):
            place_label =""
            plot_title = col
            desired_plotting_steps = int(self.desired_plotting_steps_entry_box.get())
            if desired_plotting_steps>max_time_step: #in case user inputs more timesteps than available
                desired_plotting_steps = max_time_step
                
            if desired_plotting_steps %2==0: #if even, subtract 1, avoid errors.(only works if odd for some reason)
                desired_plotting_steps = desired_plotting_steps-1
                
            t=np.arange(0,desired_plotting_steps*simulation_time_step+simulation_time_step,simulation_time_step) #(start,end,step) end in seconds. end = 1000 with ts=0.001 means you have 1000000 datapoints.

            t=t[0::int(self.nth_datapoint_entry_box.get())] #takes every nth data point. But still need to make sure the Axes are right somehow.                
          
            fig,ax=plt.subplots()
            if CONS_OR_PROD == "Cons":
                data = self.Analysis_dataframe_cons[[col]][0:desired_plotting_steps+1] 
                data = data[0::int(self.nth_datapoint_entry_box.get())]
                if self.Analysis_print_mean_value_var:
                    print("Mean: ", np.mean(data))
            if CONS_OR_PROD == "Prod":
                data = self.Analysis_dataframe_prod[[col]][0:desired_plotting_steps+1] 
                data = data[0::int(self.nth_datapoint_entry_box.get())]                
                if self.Analysis_print_mean_value_var:
                    print("Mean: ", np.mean(data))                
                
            self.Analysis_rolling_average_decision=self.Analysis_rolling_average.get()
            da_window_size = int(self.Analysis_RAWS_entry.get())  
            
            option2 = self.Analysis_plot_rolling_only_var.get()
            if option2==0:
                if place_label == "":
                    ax.plot(t, data, label = File,  color="black")
                else:
                    ax.plot(t, data, label = File+' - '+place_label, color="black")          
            
            if self.Analysis_rolling_average_decision ==1:
                data2 = data.rolling(window=da_window_size).mean()
                plt.plot(t, data2, color="red", label="Rolling Mean")         

            Analysis.standardise_plot(ax, title = plot_title, xlabel = "Time (s)",ylabel = "Molecule count")
            if self.Analysis_y_threshold_entry.get() != "":
                plt.axhline(y=float(self.Analysis_y_threshold_entry.get()), linestyle='--', color ='red', label = self.Analysis_y_threshold_graph_label.get())            
                
            if self.Analysis_plotting_text_list_entry.get() == "":
                ax.legend()
            else:
                L = ax.legend()
                L.get_texts()[0].set_text(self.Analysis_plotting_text_list_entry.get())                     

            if self.Analysis_x_lim_entry.get() != "":
                split_list = self.Analysis_x_lim_entry.get().split(", ")
                x_lim_0 = float(split_list[0])
                x_lim_1 = float(split_list[1])
                plt.xlim([x_lim_0,x_lim_1])
                
            if self.Analysis_y_lim_entry.get() != "":
                split_list = self.Analysis_y_lim_entry.get().split(", ")
                y_lim_0 = float(split_list[0])
                y_lim_1 = float(split_list[1])
                plt.ylim([y_lim_0,y_lim_1])                

            if self.Analysis_Plot_Title.get() != "":
                plt.title(self.Analysis_Plot_Title.get())
                
            if self.Analysis_Plot_Y_Axis_Label_Entry.get() != "":
                plt.ylabel(self.Analysis_Plot_Y_Axis_Label_Entry.get())                
            
            plt.show()     
            

            if self.Export_var.get() ==1:
                thename = "../saved-csvs/"+str(self.CSV_save_name.get())+".csv"
                with open(thename, 'w', newline='') as csvfile:
                    token_header = col+' Tokens'
                    fieldnames = ['Time (s)', token_header]
                    thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    thewriter.writeheader()
                    for thetime, token in zip(t,data.iloc[:,0]):
                        thewriter.writerow({'Time (s)':thetime, token_header:token})
                print("CSV Saved at " + thename)
            self.csv_listbox.destroy()
            self.csv_list_box_function() 
            self.update_truth_list()            
            
            
        def run_Analysis(self):
            self.button_2.config(text="Please Wait, Loading...", state=tk.DISABLED)
            self.button_saved_run.forget()
            self.button3.forget()
            self.run_save_name_entry.forget()
            run_save_name = self.run_save_name
            self.analysis = {}
            start_time = datetime.now()
            
            
            
            #File1 = '200k_sHFPN_Healthy_SD_01_DelaySD_01_run3_V3_TRANSITION'
            #File2 = '6e6_sHFPN_Healthy_SD_0_DelaySD_02'
            File3 = run_save_name

            
            #analysis[File1] = Analysis.load_from_file(File1)
            #analysis[File2] = Analysis.load_from_file(File2)
            self.analysis[File3] = Analysis.load_from_file(File3)
            
            execution_time = datetime.now()-start_time
            print('\n\nLoad-in Time:', execution_time)
            print("")    
            
            simulation_time_step=self.analysis[File3].time_step
            desired_plotting_steps=self.analysis[File3].final_time_step
            max_time_step = self.analysis[File3].final_time_step
            print(simulation_time_step)
            
            list_of_place_names = []
            for place in self.analysis[File3].place_ids:
                list_of_place_names.append(place)
            
            tk.Button(self.frame_in_canvas_Analysis, text = "Places", bg="grey").grid(row=0, column=0, pady=10, padx=10)
            
            #PLACE TOKENS
            for index, place_id in enumerate(list_of_place_names):
                tk.Button(self.frame_in_canvas_Analysis, cursor="cross", text=place_id, command=partial(GUI_plot, place_id, self.analysis, File3, simulation_time_step, desired_plotting_steps, max_time_step), bg="DodgerBlue3").grid(row=index+1, column=0, pady=10, padx=10)#pass value as an argument to plot  
                self.canvas2.configure(scrollregion= self.canvas2.bbox("all"))
                
            #CONSUMPTION
            tk.Button(self.frame_in_canvas_Analysis, text="Consumption Rate", bg="grey").grid(row=0, column=1, pady=10,padx=10)
            self.Analysis_dataframe_cons = self.analysis[File3].df_for_rate_analytics_cons
            CONS_OR_PROD = "Cons"
            for index, col in enumerate(self.Analysis_dataframe_cons.columns):
                tk.Button(self.frame_in_canvas_Analysis, cursor="cross", text=col, command=partial(GUI_Plot_Rate, col, self.analysis, File3, simulation_time_step, desired_plotting_steps, max_time_step, CONS_OR_PROD), bg="DodgerBlue3").grid(row=index+1, column=1,pady=10, padx=10)
                
            #Production
            tk.Button(self.frame_in_canvas_Analysis, text="Production Rate", bg="grey").grid(row=0, column=2, pady=10,padx=10)
            self.Analysis_dataframe_prod = self.analysis[File3].df_for_rate_analytics_prod
            CONS_OR_PROD = "Prod"
            for index, col in enumerate(self.Analysis_dataframe_prod.columns):
                tk.Button(self.frame_in_canvas_Analysis, cursor="cross", text=col, command=partial(GUI_Plot_Rate, col, self.analysis, File3, simulation_time_step, desired_plotting_steps, max_time_step, CONS_OR_PROD), bg="DodgerBlue3").grid(row=index+1, column=2,pady=10, padx=10)                

            self.button_2.config(text="Restart Session to Run Another Analysis", state=tk.DISABLED)
            
            
            #Saved Name Label
            SD_font = tkfont.Font(family='Helvetica', size=10, weight="bold")
            self.Label1321 = tk.Label(self.frame_in_canvas_Analysis, text="File Name:")
            self.Label1321.grid(row=0, column=3, pady=10, padx=10)
            self.Analysis_title_header_label = tk.Label(self.frame_in_canvas_Analysis, text= run_save_name, font=SD_font)

            self.Analysis_title_header_label.grid(row=0, column=4, pady=10,padx=10)
            
            #Desired Plotting Steps
            self.desired_plotting_steps_label = tk.Label(self.frame_in_canvas_Analysis, text = "Desired Plotting Steps")
            self.desired_plotting_steps_label.grid(row=1, column=3, pady=10,padx=10)
            self.desired_plotting_steps_entry_box = tk.Entry(self.frame_in_canvas_Analysis, bg="DodgerBlue3")
            self.desired_plotting_steps_entry_box.grid(row=1,column=4)
            self.desired_plotting_steps_entry_box.insert(tk.END, desired_plotting_steps)
            
            
            self.root.geometry("1250x660") #readjust size to make scrollbar visible
            
            #Plot every nth datapoint
            self.nth_datapoint_label = tk.Label(self.frame_in_canvas_Analysis, text = "Plot Every nth Data Point")
            self.nth_datapoint_label.grid(row=2, column =3, pady=10,padx=10)
            self.nth_datapoint_entry_box = tk.Entry(self.frame_in_canvas_Analysis, bg="DodgerBlue3")
            self.nth_datapoint_entry_box.grid(row=2, column=4)
            self.nth_datapoint_entry_box.insert(tk.END, 1)
  
            def Export_Enable_Disable(self):
                if self.Export_Enable_Disable_decision == 0:
                    self.CSV_save_name.config(state="normal")
                    self.Export_Enable_Disable_decision = 1
                else:
                    self.CSV_save_name.config(state = tk.DISABLED)
                    self.Export_Enable_Disable_decision = 0

  
            #Export to CSV
            self.Export_Enable_Disable_decision = 0 
            self.Export_label = tk.Label(self.frame_in_canvas_Analysis, text="Export to CSV")
            self.Export_label.grid(row=3, column=3, pady=10,padx=10)
            self.Export_var = tk.IntVar()
            self.Export_Checkbutton = tk.Checkbutton(self.frame_in_canvas_Analysis, variable=self.Export_var, command=partial(Export_Enable_Disable, self), fg="Black", selectcolor="grey42", relief=tk.GROOVE, highlightcolor="DodgerBlue3", bg="DodgerBlue3", activeforeground = "red", activebackground="red")
            self.Export_Checkbutton.grid(row=3, column=4, pady=10, padx=10)
            
            #Export to CSV Save Name
            self.CSV_save_name_label = tk.Label(self.frame_in_canvas_Analysis, text="CSV Save Name")
            self.CSV_save_name_label.grid(row=4, column=3, pady=10, padx=10)
            self.CSV_save_name = tk.Entry(self.frame_in_canvas_Analysis, bg="DodgerBlue3")
            self.CSV_save_name.grid(row=4, column=4, pady=10, padx=10)
            self.CSV_save_name.insert(tk.END, "CSV_Save_Name")
            self.CSV_save_name.config(state = tk.DISABLED)
 
            def on_click_listbox(event):
                index=self.csv_listbox.curselection()
                seltext=self.csv_listbox.get(index)
                self.csv_string = seltext            

            #MDV button
            def calculate_MDV_delay_function(self, analysis, File3):
                test = self.analysis[File3].delay_list_MDVs
                print(test)
                print(np.mean(test))
                
            self.MDV_button = tk.Button(self.frame_in_canvas_Analysis, text="Calculate MDV Delay", cursor="hand2", command=partial(calculate_MDV_delay_function, self, self.analysis, File3), bg="grey")
            self.MDV_button.grid(row=5,column=3, padx=10,pady=10)
            
            def calculate_calcium_Delay_function(self,analysis,File3):
                test = self.analysis[File3].delay_list_t_A
                test2 =self.analysis[File3].delay_list_t_B
                test3 = self.analysis[File3].delay_list_t_D
                # print(test, test2, test3)
                print("t_A:", np.mean(test),"t_B:", np.mean(test2),"t_D:", np.mean(test3))
                
                print(f"File: {File3}")
                place_id = 'p_on4'
                self.calc_and_print_mean_sd_calcium(File3, place_id)
                place_id = 'p_Ca_extra'
                self.calc_and_print_mean_sd_calcium(File3, place_id)
                place_id = 'p_on3'
                self.calc_and_print_mean_sd_calcium(File3, place_id)        
                print("Done")   
                
            self.Ca_button = tk.Button(self.frame_in_canvas_Analysis, text="Calculate Ca Delay", cursor="hand2", command=partial(calculate_calcium_Delay_function, self, self.analysis, File3), bg="grey")
            self.Ca_button.grid(row=5,column=4, padx=10,pady=10)
            
            #Rolling Average
            self.Analysis_Empty_Label111 = tk.Label(self.frame_in_canvas_Analysis, text="")
            self.Analysis_Empty_Label111.grid(row=6,column=3, pady=10,padx=10)
            def Analysis_Enable_Disable(self):
                if self.Analysis_enabled==0:
                    self.Analysis_plot_rolling_only_checkbutton.config(state="normal")
                    self.Analysis_RAWS_entry.config(state="normal")
                    self.Analysis_enabled=1
                else:
                    self.Analysis_plot_rolling_only_checkbutton.config(state=tk.DISABLED)
                    self.Analysis_RAWS_entry.config(state=tk.DISABLED)
                    self.Analysis_enabled=0
                
            self.Analysis_enabled=0
            SD_font = tkfont.Font(family='Helvetica', size=10, weight="bold")
            self.Analysis_Rolling_Header = tk.Label(self.frame_in_canvas_Analysis, text="Rolling Averages", font=SD_font)
            self.Analysis_Rolling_Header.grid(row=7, column=3, padx=10,pady=10)
            self.Analysis_rolling_average = tk.IntVar()
            self.Analysis_rolling_average_checkbox = tk.Checkbutton(self.frame_in_canvas_Analysis, var=self.Analysis_rolling_average, text="Rolling Average?", command=partial(Analysis_Enable_Disable, self))
            self.Analysis_rolling_average_checkbox.grid(row = 7, column=4, padx=10, pady=10)
    
            self.Analysis_plot_rolling_only_var = tk.IntVar()
            self.Analysis_plot_rolling_only_checkbutton = tk.Checkbutton(self.frame_in_canvas_Analysis, var=self.Analysis_plot_rolling_only_var, text="Plot Rolling Average Only?", state=tk.DISABLED)
            self.Analysis_plot_rolling_only_checkbutton.grid(row=7,column=5, padx=10,pady=10)
            
            self.Analysis_RAWS = tk.Label(self.frame_in_canvas_Analysis, text="Rolling Average Window Size")
            self.Analysis_RAWS.grid(row=8, column=3, padx=10,pady=10)
            self.Analysis_RAWS_entry = tk.Entry(self.frame_in_canvas_Analysis)
            self.Analysis_RAWS_entry.insert(tk.END, 100)
            self.Analysis_RAWS_entry.config(state=tk.DISABLED)
            self.Analysis_RAWS_entry.grid(row=8, column=4, padx=10,pady=10)
            
            self.Label_Threshold_header = tk.Label(self.frame_in_canvas_Analysis, text="Add y threshold")
            self.Label_Threshold_header.grid(row=9, column=3, padx=10,pady=10)
            self.Analysis_y_threshold_entry = tk.Entry(self.frame_in_canvas_Analysis)
            self.Analysis_y_threshold_entry.grid(row=9, column=4, padx=10, pady=10)
            self.Label_Threshold_header2 = tk.Label(self.frame_in_canvas_Analysis, text="Threshold Label")
            self.Label_Threshold_header2.grid(row=10, column=3, padx=10,pady=10)
            self.Analysis_y_threshold_graph_label = tk.Entry(self.frame_in_canvas_Analysis)
            self.Analysis_y_threshold_graph_label.grid(row=10, column=4, padx=10,pady=10)
            
            self.Analysis_plotting_text_list_label = tk.Label(self.frame_in_canvas_Analysis, text="Main Plot Legend Name")
            self.Analysis_plotting_text_list_label.grid(row=11,column=3)
            self.Analysis_plotting_text_list_entry = tk.Entry(self.frame_in_canvas_Analysis)
            self.Analysis_plotting_text_list_entry.grid(row=11,column=4)
            
            self.Analysis_x_lim_label = tk.Label(self.frame_in_canvas_Analysis, text="X Axis Limits (E.g. Input 0, 100 ', ' Comma SPACE)")
            self.Analysis_x_lim_label.grid(row=12, column=3)
            self.Analysis_x_lim_entry = tk.Entry(self.frame_in_canvas_Analysis)
            self.Analysis_x_lim_entry.grid(row=12, column=4)
            self.Analysis_y_lim_label = tk.Label(self.frame_in_canvas_Analysis, text="Y Axis Limits (Separate with ', 'Comma SPACE)", relief=tk.RIDGE)
            self.Analysis_y_lim_label.grid(row=13, column=3)
            self.Analysis_y_lim_entry = tk.Entry(self.frame_in_canvas_Analysis)
            self.Analysis_y_lim_entry.grid(row=13, column=4)    
            self.Analysis_Plot_Title_label = tk.Label(self.frame_in_canvas_Analysis, text="Plot Title", relief=tk.RAISED)
            self.Analysis_Plot_Title_label.grid(row=14, column=3)            
            self.Analysis_Plot_Title = tk.Entry(self.frame_in_canvas_Analysis)
            self.Analysis_Plot_Title.grid(row=14, column=4)
            self.Analysis_Plot_Y_Axis_Label_Label = tk.Label(self.frame_in_canvas_Analysis, text="Y Axis Label", bg="grey42", relief=tk.GROOVE)
            self.Analysis_Plot_Y_Axis_Label_Label.grid(row=15, column=3)
            self.Analysis_Plot_Y_Axis_Label_Entry = tk.Entry(self.frame_in_canvas_Analysis, bg="DodgerBlue3", relief=tk.GROOVE)
            self.Analysis_Plot_Y_Axis_Label_Entry.grid(row=15, column=4)
            self.Analysis_print_mean_value_var = tk.BooleanVar()
            self.Analysis_print_mean_value = tk.Checkbutton(self.frame_in_canvas_Analysis, var=self.Analysis_print_mean_value_var, text="Print Mean Value to Console?")
            self.Analysis_print_mean_value.grid(row=16, column=4)
            
            




        #Indent Corresponds to Analysis Page
        self.button_2 = tk.Button(self.frame5, text="Please Enter Save Name", state=tk.DISABLED, command= threading.Thread(target = partial(run_Analysis,self)).start)
        self.button_2.config(cursor="hand2")
        self.button_2.pack(side=tk.TOP)
        self.make_scrollbar_Analysis()
    def csv_list_box_function(self):
        
            def on_click_listbox(event):
                index=self.csv_listbox.curselection()
                seltext=self.csv_listbox.get(index)
                self.csv_string = seltext
            #ListBox
            self.csv_listbox = tk.Listbox(self.frame_in_canvas_CSV_Page)
            self.csv_listbox.grid(row=0, column=0, pady=10, padx=10)
            self.csv_listbox.bind('<ButtonRelease-1>', on_click_listbox) 
            
            if platform == 'darwin':
                for file in glob.glob("../saved-csvs/*.csv"):
                    file=file[14:len(file)-4]
                    self.csv_listbox.insert(tk.END, file)  
                    
            if platform == 'win32':
                for file in glob.glob("..\saved-csvs\*.csv"):
                    file=file[14:len(file)-4]
                    self.csv_listbox.insert(tk.END, file)            
    def show_saved_runs(self):
        self.frame6=tk.Frame(self.frame2)
        #self.frame6.pack(side="left", fill=tk.BOTH,expand=1)  
        self.frame6.grid(row=0,column=0,sticky="nsew")
        self.lbx = tk.Listbox(self.frame6)
        self.lbx.pack(fill=tk.BOTH, expand=1)
   
        if platform == 'darwin':
            for file in glob.glob("../saved-runs/*"):
                file=file[14:len(file)-4]
                self.lbx.insert(tk.END, file)  
                
        if platform == 'win32':
            for file in glob.glob("..\saved-runs\*"):
                file=file[14:len(file)-4]
                self.lbx.insert(tk.END, file) 
   
        def insert_run_name(self):
            self.run_save_name_entry.delete(0, tk.END)
            self.run_save_name_entry.insert(tk.END, self.saved_run_string)       
            
        def on_click_listbox(event):
            index=self.lbx.curselection()
            seltext=self.lbx.get(index)
            self.saved_run_string = seltext
            self.button_saved_run.config(state="normal")
            self.button_saved_run.config(text="Input Last Hovered Saved Run",state="normal", command=partial(insert_run_name, self))        
       
        self.lbx.bind('<ButtonRelease-1>', on_click_listbox)   

    def green_listbox_selection(self):
        for index, item in enumerate(self.truth_list):
            if item == 1:
                self.csv_listbox.itemconfig(index, bg="green", fg="white")
            else:
                self.csv_listbox.itemconfig(index, bg="white", fg="black")                

    def update_truth_list(self):
       self.truth_list = []
       for item in self.e4:
           if item in self.selection_list:
               self.truth_list.append(1)
           else:
               self.truth_list.append(0)               

    def create_list_counting_zero_runs(self, normal_list):
        """
        so in calcium, there is an array of zeros and ones. This function counts the length of zeros the span the array, and appends it to a new list and returns the list
        """
        list_2 = []
    
        count = 0    
        for index,number in enumerate(normal_list): 
            if number == 0:
                count = count+1
            if number ==1 and normal_list[index-1]==0:
                list_2.append(int(count))
                count = 0
            if number == 0 and index == (len(normal_list)-1): #So situations where we reach the end of the list and we are stuck with a zero are still counted.
                list_2.append(int(count))
        #Cut_off_the very first and last element of the list for safety reasons, to deal with potential truncated zero-runs lowering the mean.
        list_2.pop(0)
        list_2.pop()    
    
        return list_2
    
    def create_list_counting_one_runs(self, normal_list):
        """
        so in calcium, there is an array of zeros and ones. This function counts the length of zeros the span the array, and appends it to a new list and returns the list
        """
        list_2 = []
    
        count = 0    
        for index,number in enumerate(normal_list): 
            if number == 1:
                count = count+1
            if number ==0 and normal_list[index-1]==1:
                list_2.append(int(count))
                count = 0
            if number == 1 and index == (len(normal_list)-1): #So situations where we reach the end of the list and we are stuck with a zero are still counted.
                list_2.append(int(count))
        #Cut_off_the very first and last element of the list for safety reasons, to deal with potential truncated zero-runs lowering the mean.
        list_2.pop(0)
        list_2.pop()    
    
        return list_2    
    
    

    def calc_and_print_mean_sd_calcium(self, file, place_id):
        """
        This can take a long time if the list is huge (6million+ time steps).
        data is in a two dimensional form and needs to be converted to a one dimensional list.
        Calculates the Mean number of time steps until that transition contains a one token again and the SD for the place_id over the whole run
        """
        data = self.analysis[file].mean_token_history_for_places([place_id])[0:self.analysis[file].final_time_step+1] 
        list_of_lists = data.tolist()
        normal_list = [item for sublist in list_of_lists for item in sublist]    
    
        zero_runs_count_list = self.create_list_counting_zero_runs(normal_list)
        one_runs_count_list = self.create_list_counting_one_runs(normal_list) 
        mean1 = np.mean(zero_runs_count_list)
        mean2 = np.mean(one_runs_count_list)
        std1 = np.std(zero_runs_count_list)
        std2= np.std(one_runs_count_list)
        print(f"Mean Delay for {place_id}:", np.round(mean1, decimals =3), "timesteps", len(zero_runs_count_list), "counts")
        print(f"SD for {place_id}: +/-", np.round(std1, decimals=3), "timesteps or", np.round(100*std1/mean1, decimals=3), "%") 
        print("Max:", max(zero_runs_count_list), "Min:", min(zero_runs_count_list))
        #print("The very first element was:", zero_runs_count_list[0]) 
        #print("The very last element was: ", zero_runs_count_list[len(zero_runs_count_list)-1])     
        print('')
        print(f"Mean Time Active for {place_id}:", np.round(mean2, decimals =3), "timesteps", len(one_runs_count_list), "counts")
        print(f"SD for {place_id}: +/-", np.round(std2, decimals=3), "timesteps or", np.round(100*std2/mean2, decimals=3), "%") 
        print("Max:", max(one_runs_count_list), "Min:", min(one_runs_count_list))
        print('')
        print('#########################')

    def make_scrollbar_CSV_Page(self):
        self.canvas4 = tk.Canvas(self.frame11)
        self.canvas4.pack(side="left", fill=tk.BOTH, expand=1)
        self.scrollbar4 = ttk.Scrollbar(self.frame11, orient=tk.VERTICAL, command =self.canvas4.yview)
        self.scrollbar4.pack(side="left", fill=tk.Y)
        
        self.canvas4.configure(yscrollcommand=self.scrollbar4.set)
        self.canvas4.bind('<Configure>', lambda e: self.canvas4.configure(scrollregion= self.canvas4.bbox("all")))
        
        #Create another frame inside the canvas2
        self.frame_in_canvas_CSV_Page = tk.Frame(self.canvas4)
        self.canvas4.create_window((0,0), window=self.frame_in_canvas_CSV_Page, anchor="nw")   


    def Saved_Csvs_page(self):
        self.frame11 =tk.Frame(self.frame2)
        self.frame11.grid(row=0,column=0,sticky="nsew")
        self.make_scrollbar_CSV_Page()      
        
        self.csv_list_box_function()
        self.selection_list = []        
        
        def plot_csvs_function(self):
            #read all csvs, second column
            self.csv_dict={}
            print(self.selection_list, "selection list order")
            option1= self.reverse_checkbutton_var.get()
            if option1 == 1:
                option1= True
            else:
                option1= False
            self.selection_list = sorted(self.selection_list, reverse = option1)
            for index, the_csv in enumerate(self.selection_list):
                self.csv_dict[index]=pd.read_csv("../saved-csvs/"+the_csv+".csv", usecols=[0,1])
            print(self.csv_dict.keys())
            the_title = self.title_entrybox.get()
            xlabel = self.xlabel_entrybox.get()
            ylabel = self.ylabel_entrybox.get()
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            #hold plot on
            plt.title(the_title)
            self.rolling_average_decision=self.rolling_average.get()
            da_window_size = int(self.RAWS_entry.get())
            option2 = self.plot_rolling_only_var.get()
            if option2==0:
                for thecsv,key in zip(self.selection_list, self.csv_dict.keys()):
                    plt.plot(self.csv_dict[key].iloc[:,0], self.csv_dict[key].iloc[:,1], label=thecsv)
             
                           
                
            for thecsv,key in zip(self.selection_list, self.csv_dict.keys()): #So that rolling averages plot after and don't get covered up in the graph
                if self.rolling_average_decision ==1:     
                    plt.plot(self.csv_dict[key].iloc[:,0], self.csv_dict[key].iloc[:,1].rolling(window=da_window_size).mean(), label=thecsv)
            self.csv_plotting_text_list=self.csv_plotting_text_list_entry.get()
            
            #Threshold axHline
            if self.CSV_y_threshold_entry.get() != "":
                plt.axhline(y=float(self.CSV_y_threshold_entry.get()), linestyle='--', color ='red', label = self.CSV_y_threshold_graph_label.get())             
            
            #Legend
            if self.csv_plotting_text_list == "":
                pass
            else:
                split_list = self.csv_plotting_text_list.split(", ")
                L = plt.legend()
                for index,text in enumerate(split_list):
                    L.get_texts()[index].set_text(text)
            
            if self.CSV_Twin_y_lim_entry.get() != "":
                split_list = self.CSV_Twin_y_lim_entry.get().split(", ")
                y_lim_0 = float(split_list[0])
                y_lim_1 = float(split_list[1])
                plt.ylim(y_lim_0,y_lim_1)

            if self.CSV_Twin_x_lim_entry.get() != "":
                split_list = self.CSV_Twin_x_lim_entry.get().split(", ")
                x_lim_0 = float(split_list[0])
                x_lim_1 = float(split_list[1])
                plt.xlim(x_lim_0,x_lim_1)
            
            plt.show()   
            
            

                        
        
        self.Plot_csvs_button = tk.Button(self.frame_in_canvas_CSV_Page, text="Plot", cursor="hand2",command=partial(plot_csvs_function, self))
        self.Plot_csvs_button.grid(row=0, column=1, padx=10, pady=10)
        self.reverse_checkbutton_var = tk.IntVar()
        self.reverse_checkbutton = tk.Checkbutton(self.frame_in_canvas_CSV_Page, var=self.reverse_checkbutton_var, text="Reverse Plot Order?")
        self.reverse_checkbutton.grid(row=0,column=2, padx=10,pady=10)        
            
        def on_click_listbox(event):
            index=self.csv_listbox.curselection()
            seltext=self.csv_listbox.get(index)
            self.csv_string = seltext
        #BACKself.button_saved_run.config(text="Input Last Hovered Saved Run",state="normal", command=partial(insert_run_name, self))

        self.csv_listbox.bind('<ButtonRelease-1>', on_click_listbox)    
        
        #Rolling Average
        self.Empty_Label111 = tk.Label(self.frame_in_canvas_CSV_Page, text="")
        self.Empty_Label111.grid(row=7,column=0, pady=10,padx=10)
        def Enable_Disable(self):
            if self.enabled==0:
                self.plot_rolling_only_checkbutton.config(state="normal")
                self.RAWS_entry.config(state="normal")
                self.RAWS_Legend_Entry.config(state="normal")
                self.enabled=1
            else:
                self.plot_rolling_only_checkbutton.config(state=tk.DISABLED)
                self.RAWS_entry.config(state=tk.DISABLED)
                self.RAWS_Legend_Entry.config(state=tk.DISABLED)
                self.enabled=0
            
        self.enabled=0
        SD_font = tkfont.Font(family='Helvetica', size=10, weight="bold")
        self.Rolling_Header = tk.Label(self.frame_in_canvas_CSV_Page, text="Rolling Averages", font=SD_font)
  
        
        
        self.Rolling_Header.grid(row=8, column=0, padx=10,pady=10)
        self.rolling_average = tk.IntVar()
        self.rolling_average_checkbox = tk.Checkbutton(self.frame_in_canvas_CSV_Page, var=self.rolling_average, text="Rolling Average?", command=partial(Enable_Disable, self))
        self.rolling_average_checkbox.grid(row = 8, column=1, padx=10, pady=10)

        self.plot_rolling_only_var = tk.IntVar()
        self.plot_rolling_only_checkbutton = tk.Checkbutton(self.frame_in_canvas_CSV_Page, var=self.plot_rolling_only_var, text="Plot Rolling Average Only?", state=tk.DISABLED)
        self.plot_rolling_only_checkbutton.grid(row=8,column=2, padx=10,pady=10)
        
        self.RAWS = tk.Label(self.frame_in_canvas_CSV_Page, text="Rolling Average Window Size")
        self.RAWS.grid(row=9, column=0, padx=10,pady=10)
        self.RAWS_entry = tk.Entry(self.frame_in_canvas_CSV_Page)
        self.RAWS_entry.insert(tk.END, 100)
        self.RAWS_entry.config(state=tk.DISABLED)
        self.RAWS_entry.grid(row=9, column=1, padx=10,pady=10)
        
        self.CSV_Label_Threshold_header = tk.Label(self.frame_in_canvas_CSV_Page, text="Add y threshold")
        self.CSV_Label_Threshold_header.grid(row=10, column=0, padx=10,pady=10)
        self.CSV_y_threshold_entry = tk.Entry(self.frame_in_canvas_CSV_Page)
        self.CSV_y_threshold_entry.grid(row=10, column=1, padx=10, pady=10)
        self.CSV_LabeL_Threshold_header_desc = tk.Label(self.frame_in_canvas_CSV_Page, text="Input Token Number")
        self.CSV_LabeL_Threshold_header_desc.grid(row=10, column=2, padx=10, pady=10)
        self.CSV_Label_Threshold_header2 = tk.Label(self.frame_in_canvas_CSV_Page, text="Threshold Label")
        self.CSV_Label_Threshold_header2.grid(row=11, column=0, padx=10,pady=10)
        self.CSV_y_threshold_graph_label = tk.Entry(self.frame_in_canvas_CSV_Page)
        self.CSV_y_threshold_graph_label.grid(row=11, column=1, padx=10,pady=10)
        self.CSV_LabeL_Threshold_header2_desc = tk.Label(self.frame_in_canvas_CSV_Page, text="Input String")
        self.CSV_LabeL_Threshold_header2_desc.grid(row=11, column=2, padx=10, pady=10)
        
        self.RAWS_Legend_Label = tk.Label(self.frame_in_canvas_CSV_Page, text="Rolling Average Legend")
        self.RAWS_Legend_Label.grid(row=12, column=3, padx=10,pady=10)
        self.RAWS_Legend_Entry = tk.Entry(self.frame_in_canvas_CSV_Page)
        self.RAWS_Legend_Entry.grid(row=12, column=4, padx=10,pady=10)        
        self.RAWS_Legend_Entry.config(state=tk.DISABLED)
        
        
        def select_button_function(self):
            
            self.selection_list.append(self.csv_string)
            self.selection_list = list(set(self.selection_list)) #make selection list unique
            self.e4 = list(self.csv_listbox.get(0,tk.END))#get all items in listbox
            self.update_truth_list()
            print(self.truth_list)
            self.green_listbox_selection()
  

            #listbox item/using index should bg="green", then a plot button, which reads all the selected csv files.
            #store selected items to a list. so need to make a new function which reads multiple csv files, then plots it

        def deselect_button_function(self):
            self.selection_list.remove(self.csv_string)
            self.update_truth_list()
            self.green_listbox_selection()
            print(self.selection_list)
        self.select_button = tk.Button(self.frame_in_canvas_CSV_Page, text="Select", cursor="hand2", command=partial(select_button_function, self))
        self.select_button.grid(row=2,column=0, padx=10, pady=10)
        self.deselect_button = tk.Button(self.frame_in_canvas_CSV_Page, text="Deselect", cursor="hand2", command=partial(deselect_button_function, self))
        self.deselect_button.grid(row=2,column=1,padx=10, pady=10)        
                
        self.title_label = tk.Label(self.frame_in_canvas_CSV_Page, text="Plot Title")
        self.title_label.grid(column=0, row =3, padx=10,pady=10)
        self.title_entrybox = tk.Entry(self.frame_in_canvas_CSV_Page)
        self.title_entrybox.grid(column=1, row=3, padx=10,pady=10)
        self.xlabel_label = tk.Label(self.frame_in_canvas_CSV_Page, text="X Label")
        self.xlabel_label.grid(column=0, row =4, padx=10,pady=10)
        self.xlabel_entrybox = tk.Entry(self.frame_in_canvas_CSV_Page)
        self.xlabel_entrybox.grid(column=1, row=4, padx=10,pady=10)    
        self.ylabel_label = tk.Label(self.frame_in_canvas_CSV_Page, text="Y Label")
        self.ylabel_label.grid(column=0, row =5, padx=10,pady=10)
        self.ylabel_entrybox = tk.Entry(self.frame_in_canvas_CSV_Page)
        self.ylabel_entrybox.grid(column=1, row=5, padx=10,pady=10) 
        #Legend Names
        self.csv_plotting_text_list_label = tk.Label(self.frame_in_canvas_CSV_Page, text="Legend Names")
        self.csv_plotting_text_list_label.grid(row=6,column=0)
        self.csv_plotting_text_list_entry = tk.Entry(self.frame_in_canvas_CSV_Page)
        self.csv_plotting_text_list_entry.grid(row=6,column=1)
        self.csv_plotting_text_help_label = tk.Label(self.frame_in_canvas_CSV_Page, text="Separate strings by ', '")
        self.csv_plotting_text_help_label.grid(row=6,column=2)      

        def twin_plot_function(self):
            
            #read all csvs, second column
            self.csv_dict={}
            print(self.selection_list, "selection list order")
            #Reverse Plot Order
            option1= self.reverse_checkbutton_var.get()
            if option1 == 1:
                option1= True
            else:
                option1= False
            self.selection_list = sorted(self.selection_list, reverse = option1)
            
            #Save Csv Token Columns to dictionary
            for index, the_csv in enumerate(self.selection_list):
                self.csv_dict[index]=pd.read_csv("../saved-csvs/"+the_csv+".csv", usecols=[0,1])
            print(self.csv_dict.keys())
            
            #Initialise Subplots
            fig, ax1 = plt.subplots()
            
            #Get Plot Parameters
            the_title = self.title_entrybox.get()
            xlabel = self.xlabel_entrybox.get()
            ylabel = self.ylabel_entrybox.get()

            #Set Plot Parameters
            ax1.set_xlabel(xlabel)
            ax1.set_ylabel(ylabel)
            ax1.title.set_text(the_title)
            
            #Plot Twin Y Axes
            option2 = self.plot_rolling_only_var.get()
            if option2==0:
                #for thecsv,key in zip(self.selection_list, self.csv_dict.keys()):
                ax2 = ax1.twinx()
                
                ax1.set_zorder(1)
                ax2.set_zorder(2)
                ax1.patch.set_visible(True)                
                ax2.patch.set_visible(False)
                ax2.grid(b=False)
                
                
                
                ax1.plot(self.csv_dict[0].iloc[:,0], self.csv_dict[0].iloc[:,1], label=self.selection_list[0], color='k')
                ax2.plot(self.csv_dict[1].iloc[:,0], self.csv_dict[1].iloc[:,1], label=self.selection_list[1], color='tab:blue')
                ax2.set_ylabel(self.second_ylabel.get())
            if self.CSV_Twin_y_lim_entry.get() != "":
                split_list = self.CSV_Twin_y_lim_entry.get().split(", ")
                y_lim_0 = float(split_list[0])
                y_lim_1 = float(split_list[1])
                ax1.set_ylim([y_lim_0,y_lim_1])
                
            
            if self.CSV_Twin_y_lim_entry2.get() != "":    
                split_list2 = self.CSV_Twin_y_lim_entry2.get().split(", ")
                y_lim2_0 = float(split_list2[0])
                y_lim2_1 = float(split_list2[1])
                ax2.set_ylim([y_lim2_0,y_lim2_1])        

            if self.CSV_Twin_x_lim_entry.get() != "":
                split_list = self.CSV_Twin_x_lim_entry.get().split(", ")
                x_lim_0 = float(split_list[0])
                x_lim_1 = float(split_list[1])
                ax1.set_xlim([x_lim_0,x_lim_1])
                
            
            if self.CSV_Twin_x_lim_entry2.get() != "":    
                split_list2 = self.CSV_Twin_x_lim_entry2.get().split(", ")
                x_lim2_0 = float(split_list2[0])
                x_lim2_1 = float(split_list2[1])
                ax2.set_xlim([x_lim2_0,x_lim2_1])                                       
                
            ax1.tick_params(axis="y", labelcolor='k')
            ax2.tick_params(axis="y", labelcolor='tab:blue')

            fig.tight_layout()
            self.align_ticks = 0
            if self.align_ticks == 1:  
                minresax1 = 5
                minresax2 = 5
                
                ax1ylims = ax1.get_ybound()
                ax2ylims = ax2.get_ybound()
                ax1factor = minresax1 * 6
                ax2factor = minresax2 * 6
                ax1.set_yticks(np.linspace(ax1ylims[0],
                                           ax1ylims[1]+(ax1factor -
                                           (ax1ylims[1]-ax1ylims[0]) % ax1factor) %
                                           ax1factor,
                                           7))
                ax2.set_yticks(np.linspace(ax2ylims[0],
                                           ax2ylims[1]+(ax2factor -
                                           (ax2ylims[1]-ax2ylims[0]) % ax2factor) %
                                           ax2factor,
                                           7))            
            
 
            
            # #Plot Rolling Average
            # for thecsv,key in zip(self.selection_list, self.csv_dict.keys()): #So that rolling averages plot after and don't get covered up in the graph
            #Rolling Average
            self.rolling_average_decision=self.rolling_average.get()
            da_window_size = int(self.RAWS_entry.get())            
            if self.rolling_average_decision ==1:             
                ax1.plot(self.csv_dict[0].iloc[:,0], self.csv_dict[0].iloc[:,1].rolling(window=da_window_size).mean(), label=self.RAWS_Legend_Entry.get())
            
            
            #Threshold axHline
            if self.CSV_y_threshold_entry.get() != "":
                if self.CSV_Threshold_To_TwinPlot_var:
                    ax1.axhline(y=float(self.CSV_y_threshold_entry.get()), linestyle='--', color ='red', label = self.CSV_y_threshold_graph_label.get())         
                else:
                    ax2.axhline(y=float(self.CSV_y_threshold_entry.get()), linestyle='--', color ='red', label = self.CSV_y_threshold_graph_label.get())        
            
            #Twin Legend
            self.csv_plotting_text_list=self.csv_plotting_text_list_entry.get()
            if self.csv_plotting_text_list == "":
                lines, labels = ax1.get_legend_handles_labels()
                lines2, labels2 = ax2.get_legend_handles_labels()
                ax2.legend(lines + lines2, labels + labels2, loc=2)
            else:
                split_list = self.csv_plotting_text_list.split(", ")
                lines, labels = ax1.get_legend_handles_labels()
                lines2, labels2 = ax2.get_legend_handles_labels()
                labels[0] = split_list[0]
                labels2[0] = split_list[1]
                ax2.legend(lines + lines2, labels + labels2, loc=2)
               
                    


            
            plt.show()           
        
        self.Twin_plot_button = tk.Button(self.frame_in_canvas_CSV_Page, text="Twin Plot", command = partial(twin_plot_function, self))
        self.Twin_plot_button.grid(row=0, column=3, padx=10,pady=10)
        self.second_ylabel_Label = tk.Label(self.frame_in_canvas_CSV_Page, text="2nd Y Label")
        self.second_ylabel_Label.grid(row=1, column=3, padx=10, pady=10)
        self.second_ylabel = tk.Entry(self.frame_in_canvas_CSV_Page)
        self.second_ylabel.grid(row=1, column=4, padx=10, pady=10)
        
        self.CSV_Twin_y_lim_Label = tk.Label(self.frame_in_canvas_CSV_Page, text="YLimit 1")
        self.CSV_Twin_y_lim_Label.grid(row=2, column=3, padx=10, pady=10)
        self.CSV_Twin_y_lim_entry = tk.Entry(self.frame_in_canvas_CSV_Page)
        self.CSV_Twin_y_lim_entry.grid(row=2, column=4, padx=10, pady=10)
        self.CSV_Twin_y_lim_Label2 = tk.Label(self.frame_in_canvas_CSV_Page, text="YLimit 2")
        self.CSV_Twin_y_lim_Label2.grid(row=3, column=3, padx=10, pady=10)        
        self.CSV_Twin_y_lim_entry2=tk.Entry(self.frame_in_canvas_CSV_Page)
        self.CSV_Twin_y_lim_entry2.grid(row=3, column=4, padx=10, pady=10)
        
        self.CSV_Twin_x_lim_Label = tk.Label(self.frame_in_canvas_CSV_Page, text="XLimit 1")
        self.CSV_Twin_x_lim_Label.grid(row=4, column=3, padx=10, pady=10)
        self.CSV_Twin_x_lim_entry = tk.Entry(self.frame_in_canvas_CSV_Page)
        self.CSV_Twin_x_lim_entry.grid(row=4, column=4, padx=10, pady=10)
        self.CSV_Twin_x_lim_Label2 = tk.Label(self.frame_in_canvas_CSV_Page, text="XLimit 2")
        self.CSV_Twin_x_lim_Label2.grid(row=5, column=3, padx=10, pady=10)        
        self.CSV_Twin_x_lim_entry2=tk.Entry(self.frame_in_canvas_CSV_Page)
        self.CSV_Twin_x_lim_entry2.grid(row=5, column=4, padx=10, pady=10)   
        self.CSV_Threshold_To_TwinPlot_var = tk.BooleanVar()
        self.CSV_Threshold_To_TwinPlot_Checkbutton = tk.Checkbutton(self.frame_in_canvas_CSV_Page, text="Add Threshold to Twin Plot?", var=self.CSV_Threshold_To_TwinPlot_var)
        self.CSV_Threshold_To_TwinPlot_Checkbutton.grid(row=6, column=3)
        
        
        

    def run_sHFPN(self):
        self.lb.itemconfig(7, fg="red")
        self.Safe_Exit_Required = True
        self.Safe_Exit_Now = False
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
        
        #Rewrite Place Inputs
        self.PD_pn.set_place_tokens(value=it_p_LRRK2_mut, place_id="p_LRRK2_mut")
        self.PD_pn.set_place_tokens(value=it_p_GBA1, place_id="p_GBA1")
        self.PD_pn.set_place_tokens(value=it_p_VPS35, place_id="p_VPS35")
        self.PD_pn.set_place_tokens(value=it_p_DJ1, place_id="p_DJ1")
        self.PD_pn.set_place_tokens(value=it_p_NPT200, place_id="p_NPT200")
        self.PD_pn.set_place_tokens(value=it_p_DNL151, place_id="p_DNL151")
        self.PD_pn.set_place_tokens(value=it_p_LAMP2A, place_id="p_LAMP2A")
   
        
        #Disable Run HFPN Button
        self.button_1.config(state=tk.DISABLED)
        self.button_1.config(text="Running Simulation... Please bear with Lag...")
        
            
        self.PD_pn.set_time_step(time_step = time_step_size) #unit = s/A.U. 
        ## Define places

        
  

        #Set the Input Stochastic Parameter Values
        for index,value in enumerate(self.transitions_entry_box_dict):
            str_index = str(index) #stringed number is the key of these dictionaries
            SD_value = float(self.transitions_entry_box_dict[str_index].get()) #float because entry box value is initially a string
            transition_id = list(self.PD_pn.transitions)[index] #get the transition id (dict key) from a list of all the transitions in this dict.
            self.PD_pn.set_1st_stochastic_parameter(SD_value, transition_id)
            if self.PD_pn.transitions[transition_id].DiscreteFlag=="yes": #DiscreteFlag flags discrete transitions
                Delay_SD_Value = float(self.transitions_entry_box_Discrete_SD[str_index].get())
                self.PD_pn.set_2nd_stochastic_parameter(Delay_SD_Value, transition_id)
                
        #debugging Stochastic Parameters
        for index,value in enumerate(self.transitions_entry_box_dict):
            str_index = str(index)             
            transition_id = list(self.PD_pn.transitions)[index] 
            print(self.PD_pn.transitions[transition_id].stochastic_parameters)


        # #BEFORE FOR LOOP
        # for index,value in enumerate(self.transitions_consumption_checkboxes_dict):
        #     transition_id = list(self.PD_pn.transitions)[index]
        #     print(self.PD_pn.transitions[transition_id].collect_rate_analytics, "before For Loop")
        
            
        #FOR LOOP TO SET COLLECT #Set the Collect Rate Analytics Decisions Consumption
        for index,value in enumerate(self.transitions_consumption_checkboxes_dict):
            str_index = str(index)
            Integer_value = self.consump_checkbox_variables_dict[str_index].get() # 1 means checked, 0 means not.
            #print(type(Integer_value))
            transition_id = list(self.PD_pn.transitions)[index]
            self.PD_pn.set_consumption_collect_decision(Integer_value,transition_id)
            #print(self.PD_pn.transitions[transition_id].collect_rate_analytics, "in cons for loop") 
            
        #AFTER FOR LOOP  
        for index,value in enumerate(self.transitions_consumption_checkboxes_dict): #DEBUGGING
            transition_id = list(self.PD_pn.transitions)[index]
            print(self.PD_pn.transitions[transition_id].collect_rate_analytics, "after cons for loops")             
            
        # for index,value in enumerate(self.transitions_consumption_checkboxes_dict): #DEBUGGING
        #     transition_id = list(self.PD_pn.transitions)[index]
        #     APPENDED_LIST = []
            
        #     self.PD_pn.transitions[transition_id].collect_rate_analytics = APPENDED_LIST
        #     print(self.PD_pn.transitions[transition_id].collect_rate_analytics, "after cons for loops")           
            
        #Set the Collect Rate Analytics Decisions Production
        for index,value in enumerate(self.transitions_production_checkboxes_dict):
            str_index = str(index)
            Integer_value = self.produc_checkbox_variables_dict[str_index].get() # 1 means checked, 0 means not.
            transition_id = list(self.PD_pn.transitions)[index]
            self.PD_pn.set_production_collect_decision(integer = Integer_value, transition_id=transition_id)
            #print(self.PD_pn.transitions[transition_id].collect_rate_analytics, "in prod for loop")
            
        for index,value in enumerate(self.transitions_consumption_checkboxes_dict): #DEBUGGING
            transition_id = list(self.PD_pn.transitions)[index]
            #print(self.PD_pn.transitions[transition_id].collect_rate_analytics, "after both for loops")    
            
      
        
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
        
        
        GUI_App = self
        
        start_time = datetime.now()
        self.PD_pn.run_many_times(number_runs=number_runs, number_time_steps=number_time_steps, GUI_App=GUI_App)
        analysis = Analysis(self.PD_pn)
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
        run_save_name = self.AD_HFPN_run_save_name
        number_time_steps = int(self.AD_HFPN_number_of_timesteps)
        time_step_size = float(self.AD_HFPN_timestep_size)
        # cholSD = float(self.AD_HFPN_CholSD)
        # DelaySD = float(self.AD_HFPN_CalciumSD) 
        it_p_ApoE = self.AD_ApoE4_var.get()
        it_p_CD33 = self.AD_CD33_var.get()
        it_p_age = self.AD_Aged_var.get()
        
        #Rewrite Place Inputs
        self.AD_pn.set_place_tokens(value=it_p_ApoE, place_id="p_ApoE") # gene, risk factor in AD
        self.AD_pn.set_place_tokens(value=it_p_age, place_id="p_age")
        self.AD_pn.set_place_tokens(value=it_p_CD33, place_id='p_CD33') # 80 years old, risk factor in AD for BACE1 activity increase       
        
        
        #Disable Run HFPN Button
        self.AD_button_1.config(state=tk.DISABLED)
        self.AD_button_1.config(text="Running Simulation... Please bear with Lag...")
       
        
       # Initialize an empty HFPN #HERE
        
        self.AD_pn.set_time_step(time_step = time_step_size)      
  
        #Set the Input Stochastic Parameter Values
        for index,value in enumerate(self.transitions_entry_box_dict):
            str_index = str(index) #stringed number is the key of these dictionaries
            SD_value = float(self.transitions_entry_box_dict[str_index].get()) #float because entry box value is initially a string
            transition_id = list(self.AD_pn.transitions)[index] #get the transition id (dict key) from a list of all the transitions in this dict.
            
            self.AD_pn.set_1st_stochastic_parameter(SD_value, transition_id)
            if self.AD_pn.transitions[transition_id].DiscreteFlag=="yes": #DiscreteFlag flags discrete transitions
                Delay_SD_Value = float(self.transitions_entry_box_Discrete_SD[str_index].get())
                self.AD_pn.set_2nd_stochastic_parameter(Delay_SD_Value, transition_id)

        #Set the Collect Rate Analytics Decisions Consumption
        for index,value in enumerate(self.transitions_consumption_checkboxes_dict):
            str_index = str(index)
            Integer_value = self.consump_checkbox_variables_dict[str_index].get() # 1 means checked, 0 means not.
            transition_id = list(self.AD_pn.transitions)[index]
            self.AD_pn.set_consumption_collect_decision(Integer_value,transition_id)
         
            
        for index,value in enumerate(self.transitions_consumption_checkboxes_dict): #DEBUGGING
            transition_id = list(self.AD_pn.transitions)[index]
                       
            
    
        #Set the Collect Rate Analytics Decisions Production
        for index,value in enumerate(self.transitions_production_checkboxes_dict):
            str_index = str(index)
            Integer_value = self.produc_checkbox_variables_dict[str_index].get() # 1 means checked, 0 means not.
            transition_id = list(self.AD_pn.transitions)[index]
            self.AD_pn.set_production_collect_decision(integer = Integer_value, transition_id=transition_id)
         
            
        for index,value in enumerate(self.transitions_consumption_checkboxes_dict): #DEBUGGING
            transition_id = list(self.AD_pn.transitions)[index]
   
    

            
        GUI_App = self
        
        start_time = datetime.now()
        self.AD_pn.run_many_times(number_runs=number_runs, number_time_steps=number_time_steps, GUI_App=GUI_App)
        analysis = Analysis(self.AD_pn)
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
        
    def safe_exit(self):
        self.root.update()
        self.root.destroy()
        sys.exit()
      
             


 
   



def main():
    app = sHFPN_GUI_APP()
    def on_closing():
        if app.Safe_Exit_Required == True:
            if messagebox.askokcancel("Quit", "Please Click Safe Exit Button"):
                print("")
        else:
            app.root.destroy()
    app.root.protocol("WM_DELETE_WINDOW", on_closing)
    app.root.mainloop()   
    # del app
    # gc.collect()
    # get_ipython().magic('reset -sf')
    print("Test")
    
    
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

    # self.root.bind("<Control-l>", lambda x: self.hide()) #Unnecessary feature... to be removed
    # self.hidden=0

    # def hide(self): #to be removed
    #     if self.hidden == 0:
    #         self.frame1.destroy()
    #         self.hidden=1
    #     elif self.hidden==1:
    #         self.frame2.destroy()
    #         self.hidden=0
    #         self.Left_Sidebar()
    #         self.Right_Output()




    
if __name__ == "__main__":
    main()