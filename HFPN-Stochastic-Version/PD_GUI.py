# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 20:19:19 2021

@author: brand
"""

import tkinter as tk
from tkinter import ttk
import glob



class sHFPN_GUI_APP:
    def __init__(self):
        self.root = tk.Tk()
        self.root.iconbitmap(r'mngicon.ico')
        
        self.root.title("sHFPN GUI")
        self.root.geometry("700x500")
        self.Left_Sidebar()
        self.Right_Output()
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
        self.lb.insert(tk.END, "Inputs","Run sHFPN","Analysis")
        def callback(event):
            selection = event.widget.curselection()
            if selection:
                index=selection[0] #selection is a tuple, first item of tuple gives index
                data=event.widget.get(index)
                if data == "Inputs":
                    self.frame2.destroy()
                    self.Inputs_Page()
                    #call function which destroys the corresponding frames and displays a new frame important for inputs
                if data == "Run sHFPN":
                    self.frame2.destroy()
                    self.Run_sHFPN_Page()
                    
                if data == "Analysis":
                    self.frame2.destroy()
                    self.Analysis_page()
                    
                

        self.lb.bind("<<ListboxSelect>>", callback)
    
        #***Select item in Listbox and Display Corresponding output in Right_Output
        #self.lb.bind("<<ListboxSelect>>", Lambda x: show)
 
    def make_scrollbar(self):
        self.canvas = tk.Canvas(self.frame2)
        self.canvas.pack(side="right", fill=tk.BOTH, expand=1)
        
        self.scrollbar = ttk.Scrollbar(self.frame2, orient=tk.VERTICAL, command =self.canvas.yview)
        self.scrollbar.pack(side="right", fill=tk.Y)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion= self.canvas.bbox("all")))
        
        #Create another frame inside the canvas
        self.frame_in_canvas = tk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.frame_in_canvas, anchor="nw")
        

    def Right_Output(self):
        self.frame2= tk.Frame(self.root)
        self.frame2.pack(side="left", fill=tk.BOTH, expand=1)
        self.txt = tk.Text(self.frame2)
        self.txt.pack(fill=tk.BOTH, expand=1) 
        
    def Inputs_Page(self):
        self.frame2=tk.Frame(self.root)
        
        self.frame2.pack(side="left", fill=tk.BOTH,expand=1)
        self.e = tk.Entry(self.frame2)
        self.e.pack()
        
    def Run_sHFPN_Page(self):
        self.frame2=tk.Frame(self.root)
        self.frame2.pack(side="left", fill=tk.BOTH,expand=1)
        self.button_1 = tk.Button(self.frame2, text="Run sHFPN")
        self.button_1.pack(side=tk.TOP)
        self.make_scrollbar()
        
    def Analysis_page(self):
        self.frame2=tk.Frame(self.root)
        self.frame2.pack(side="left", fill=tk.BOTH,expand=1)
        self.button_2 = tk.Button(self.frame2, text="Run Analysis")
        self.button_2.pack(side=tk.TOP)
        self.make_scrollbar()
    
    
    def hide(self):
        if self.hidden == 0:
            self.frame1.destroy()
            self.hidden=1
        elif self.hidden==1:
            self.frame2.destroy()
            self.hidden=0
            self.Left_Sidebar()
            self.Right_Output()
                
   

            
            
           

        
  
        

app = sHFPN_GUI_APP()
app.root.mainloop()

#Old Features
    # def Right_Output(self):
    #     self.frame2= tk.Frame(self.root)
    #     self.frame2.pack(side="left", fill=tk.BOTH, expand=1)
    #     self.txt = tk.Text(self.frame2)
    #     self.txt.pack(fill=tk.BOTH, expand=1) 



                # if data == "Inputs":
                #     #destroy frame2 and create input frame
                #     self.frame2.destroy()
                #     self.Inputs_Page()
                    
                # if data == "Run sHFPN":
                #     self.frame2.destroy()
                #     self.Run_sHFPN_Page()
                    
                # if data == "Analysis":
                #     self.frame2.destroy()
                #     self.Analysis_page()
                # if data == "Saved Runs":
                #     self.frame2.destroy()
                #     self.show_saved_runs()