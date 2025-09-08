import os
import time
import math
import random
import numpy as np
import pandas as pd
from uuid import uuid4
import matplotlib.pyplot as plt
from itertools import permutations

import googlemaps
import customtkinter as ctk
from datetime import datetime
from dotenv import load_dotenv
from tkintermapview import TkinterMapView
from PIL import Image, ImageFont, ImageDraw


#app window
class App(ctk.CTk):

    #variables
    width = 864
    height = 614.4

    load_dotenv()
    api_key = os.getenv('api_key')
    maps = googlemaps.Client(key=api_key)

    start = None
    priority = []
    packages = []
    end = None

    init_p = 0.2
    alpha = 1
    beta = 2
    added_p = 10
    evap_rate = 0.1
    ants = 100

    def __init__(self):
        super().__init__()

        # window settings
        self.title("EasyNav: Easy Navigation Software")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(0, 0)
        self.configure(fg_color='#f3f2f2')
        current_path = os.path.dirname(os.path.realpath(__file__))

        #images
        self.header_logo = ctk.CTkImage(Image.open(current_path+"/assets/logo_lpb.png").resize((213, 79), Image.LANCZOS), size=(213, 79))
        #fonts
        self.REGULAR = current_path+"/assets/Nexa-ExtraLight.ttf"
        self.BOLD = current_path+"/assets/Nexa-Heavy.ttf"

        #navigation page
        self.header = ctk.CTkFrame(self, height=79, width=self.width, fg_color="#f3f2f2", corner_radius=0)
        self.seperator1 = ctk.CTkFrame(self, height=2.4, width=self.width, fg_color="black", corner_radius=0)
        self.inputbar = ctk.CTkFrame(self, height=533, width=183, fg_color="#f3f2f2", corner_radius=0)
        self.seperator2 = ctk.CTkFrame(self, height=533, width=2.4, fg_color="black", corner_radius=0)
        self.map = ctk.CTkFrame(self, height=533, width=506.4, fg_color="green", corner_radius=0)
        self.seperator3 = ctk.CTkFrame(self, height=533, width=2.4, fg_color="black", corner_radius=0)
        self.outputbar = ctk.CTkFrame(self, height=533, width=183, fg_color="#dbd4d4", corner_radius=0)

        #header
        self.small_logo = ctk.CTkLabel(self.header, image=self.header_logo, width=213, height=79, text=None, fg_color="transparent")

        #input bar
        self.input_btn = ctk.CTkButton(self.inputbar, image=self.custom_text("input dests", self.BOLD, "#ffffff", 19.8, "#5170ff"), text=None, fg_color="#5170ff", hover_color="#5170ff", width=148.2, height=35.4, corner_radius=28.8 ,command=self.get_destinations)
        self.check_btn = ctk.CTkButton(self.inputbar, image=self.custom_text("check dests", self.BOLD, "#ffffff", 19.8, "#5170ff"), text=None, fg_color="#5170ff", hover_color="#5170ff", width=148.2, height=35.4, corner_radius=28.8 ,command=self.edit_destinations)

        #output bar
        self.total_dist_lbl = ctk.CTkLabel(self.outputbar, image=self.custom_text("total distance", self.BOLD, "#727272", 12.7, "#dbd4d4"), text=None, fg_color="#dbd4d4", width=148.2, height=14.4)
        self.total_dist_val = ctk.CTkLabel(self.outputbar, image=self.custom_text("10 km", self.BOLD, "#ffffff", 42, "#dbd4d4"), text=None, fg_color="#dbd4d4", width=148.2, height=40.2)
        self.total_time_lbl = ctk.CTkLabel(self.outputbar, image=self.custom_text("total time", self.BOLD, "#727272", 12.7, "#dbd4d4"), text=None, fg_color="#dbd4d4", width=148.2, height=14.4)
        self.total_time_val = ctk.CTkLabel(self.outputbar, image=self.custom_text("5 hours\n13 mins", self.BOLD, "#ffffff", 42, "#dbd4d4"), text=None, fg_color="#dbd4d4", width=148.2, height=80.4)
        self.start_time_lbl = ctk.CTkLabel(self.outputbar, image=self.custom_text("start time", self.BOLD, "#727272", 12.7, "#dbd4d4"), text=None, fg_color="#dbd4d4", width=148.2, height=14.4)
        self.start_time_val = ctk.CTkLabel(self.outputbar, image=self.custom_text("06.14", self.BOLD, "#ffffff", 42, "#dbd4d4"), text=None, fg_color="#dbd4d4", width=148.2, height=40.2)
        self.end_time_lbl = ctk.CTkLabel(self.outputbar, image=self.custom_text("end time", self.BOLD, "#727272", 12.7, "#dbd4d4"), text=None, fg_color="#dbd4d4", width=148.2, height=14.4)
        self.end_time_val = ctk.CTkLabel(self.outputbar, image=self.custom_text("11.27", self.BOLD, "#ffffff", 42, "#dbd4d4"), text=None, fg_color="#dbd4d4", width=148.2, height=40.2)

        self.startnav_btn = ctk.CTkButton(self.outputbar, image=self.custom_text("start nav", self.BOLD, "#ffffff", 18, "#ff4848"), text=None, fg_color="#ff4848", hover_color="#ff4848", width=148.2, height=35.4, corner_radius=28.8 ,command=None)

        #map
        self.map_widget = TkinterMapView(self.map, height=532.8, width=506.4)
        self.map_widget.set_position(42.48144, -71.15103)
        self.map_widget.set_tile_server("https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", max_zoom=22)
        self.map_widget.set_zoom(19)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=0)

        self.header.grid(row=0, column=0, columnspan=5, sticky="nsew")
        self.seperator1.grid(row=1, column=0, columnspan=5, sticky="nsew")
        self.inputbar.grid(row=2, column=0, sticky="nsew")
        self.seperator2.grid(row=2, column=1, sticky="nsew")
        self.map.grid(row=2, column=2, sticky="nsew")
        self.seperator3.grid(row=2, column=3, sticky="nsew")
        self.outputbar.grid(row=2, column=4, sticky="nsew")

        self.header.grid_columnconfigure(0, weight=0)
        self.header.grid_columnconfigure(1, weight=1)
        self.header.grid_columnconfigure(2, weight=0)

        self.small_logo.grid(row=0, column=2, padx=(0, 10))

        self.inputbar.grid_rowconfigure(0, weight=0)
        self.inputbar.grid_rowconfigure(1, weight=0)
        self.inputbar.grid_rowconfigure(2, weight=1)
        self.inputbar.grid_rowconfigure(3, weight=0)

        self.inputbar.grid_columnconfigure(0, weight=1)
        self.inputbar.grid_columnconfigure(1, weight=0)
        self.inputbar.grid_columnconfigure(2, weight=1)
        self.inputbar.grid_propagate(False)

        self.input_btn.grid(row=0, column=1, pady=(50, 10), sticky="")
        self.check_btn.grid(row=1, column=1, pady=10)

        self.outputbar.grid_rowconfigure(0, weight=0)
        self.outputbar.grid_rowconfigure(1, weight=0)
        self.outputbar.grid_rowconfigure(2, weight=0)
        self.outputbar.grid_rowconfigure(3, weight=0)
        self.outputbar.grid_rowconfigure(4, weight=0)
        self.outputbar.grid_rowconfigure(5, weight=0)
        self.outputbar.grid_rowconfigure(6, weight=0)
        self.outputbar.grid_rowconfigure(7, weight=0)
        self.outputbar.grid_rowconfigure(8, weight=0)

        self.outputbar.grid_columnconfigure(0, weight=1)
        self.outputbar.grid_columnconfigure(1, weight=0)
        self.outputbar.grid_columnconfigure(2, weight=1)
        self.outputbar.grid_propagate(False)

        self.total_dist_lbl.grid(row=0, column=1, pady=(50, 10))
        self.total_dist_val.grid(row=1, column=1)
        self.total_time_lbl.grid(row=2, column=1, pady=10)
        self.total_time_val.grid(row=3, column=1, pady=(0,20))
        self.start_time_lbl.grid(row=4, column=1, pady=10)
        self.start_time_val.grid(row=5, column=1)
        self.end_time_lbl.grid(row=6, column=1, pady=10)
        self.end_time_val.grid(row=7, column=1)

        self.startnav_btn.grid(row=8, column=1, pady=(30, 0))

        self.map_widget.grid(row=0, column=0, sticky="nsew")
    
    def custom_text(self, text, font, color, fontsize, bgcolor, anchor="lt", pad_right=0):
        #load font
        font = ImageFont.truetype(font=font, size=fontsize)

        #get size
        dummy_image = Image.new(mode="RGBA", size=(1, 1))
        dummy_draw = ImageDraw.Draw(dummy_image)
        text = text.split("\n") #seperate by newline (enter)
        left, top, right, bottom = dummy_draw.textbbox((0, 0), text=max(text, key=len), font=font, anchor=anchor)
        width = right - left + 10 + pad_right#10px padding
        height = (bottom - top + 10) * len(text)

        #create img
        image = Image.new(mode="RGBA", size=(width, height), color=bgcolor)
        draw = ImageDraw.Draw(image)
        draw.fontmode = "L"
        for i, line in enumerate(text):
            draw.text(xy=(5, 5+height/len(text)*i), text=line, font=font, fill=color, anchor=anchor)
        image = ctk.CTkImage(image, size=(width,height))
        return image
    
    def get_destinations(self):
        input_window = input_dest_window(self, self.maps, self.BOLD, self.REGULAR)
        print(self.priority)
        print(self.packages)
    
    def edit_destinations(self):
        edit_window = edit_dest_window(self, self.maps, self.BOLD, self.REGULAR)

#input destinations
class input_dest_window(ctk.CTkToplevel):
    width = 450
    height = 250
    list = []

    def __init__(self, master, maps, bold_font, regular_font):
        super().__init__(master=master)
        self.maps = maps
        self.session_token = uuid4().hex
        self.title("Choose your destinations")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(0, 0)
        self.configure(fg_color='#727272')

        #widgets
        self.label = ctk.CTkLabel(self, image=master.custom_text("input destination", bold_font, "white", 12.7, "#727272"), text=None, fg_color="#727272", height=14.4)
        self.entry = ctk.CTkEntry(self, placeholder_text="Enter Address", width=400, font=("Helvetica", 18))
        self.entry.bind("<Return>", self.get_results)

        self.button0 = ctk.CTkButton(self, text="", corner_radius=None, fg_color="#dbd4d4", text_color="black", hover_color="#6c6969", width=400, height=36, command=lambda: self.return_destination(0, master))
        self.button1 = ctk.CTkButton(self, text="", corner_radius=None, fg_color="#dbd4d4", text_color="black", hover_color="#6c6969",width=400, height=36, command=lambda: self.return_destination(1, master))
        self.button2 = ctk.CTkButton(self, text="", corner_radius=None, fg_color="#dbd4d4", text_color="black", hover_color="#6c6969",width=400, height=36, command=lambda: self.return_destination(2, master))
        self.button3 = ctk.CTkButton(self, text="", corner_radius=None, fg_color="#dbd4d4", text_color="black", hover_color="#6c6969",width=400, height=36, command=lambda: self.return_destination(3, master))
        self.buttons = [self.button0, self.button1, self.button2, self.button3]

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=1)

        self.label.grid(row=0, column=1, sticky="w", pady=(10, 0))
        self.entry.grid(row=1, column=1, pady=(0, 20))

    def get_results(self, event):
        autocomplete = self.maps.places_autocomplete(input_text=self.entry.get(), session_token=self.session_token)
        self.list = [i["description"] for i in autocomplete]
        if len(self.list) > 0:
            self.list = self.list[:4]
            for i in range(len(self.list)):
                self.buttons[i].grid(row=2+i, column=1, pady=(0,2))
                self.buttons[i].configure(text=self.list[i][:55])

    def return_destination(self, index, master):
        dest = self.list[index]
        if dest != "":
            if not dest in master.packages and not dest in master.priority:
                master.packages.append(dest)

            self.destroy()

#edit destinations
class edit_dest_window(ctk.CTkToplevel):
    width = 450
    height = 250
    list = []

    def __init__(self, master, maps, bold_font, regular_font):
        super().__init__(master=master)
        self.maps = maps
        self.title("Edit your destinations")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(0, 0)
        self.configure(fg_color='#727272')

        self.priority = master.priority
        self.packages = master.packages
        self.priority_btns = []
        self.package_btns = []
        self.selected = []

        #widgets
        self.prioritize_btn = ctk.CTkButton(self, image=master.custom_text("Prioritize", bold_font, "#ffffff", 14, "#5170ff"), text=None, fg_color="#5170ff", hover_color="#5170ff", width=133.33, height=36, corner_radius=28.8 ,command=self.prioritize)
        self.delete_btn = ctk.CTkButton(self, image=master.custom_text("Delete", bold_font, "#ffffff", 14, "#5170ff"), text=None, fg_color="#5170ff", hover_color="#5170ff", width=133.33, height=36, corner_radius=28.8 ,command=self.delete)
        self.done_btn = ctk.CTkButton(self, image=master.custom_text("Done", bold_font, "#ffffff", 14, "#ff4848"), text=None, fg_color="#ff4848", hover_color="#ff4848", width=133.33, height=36, corner_radius=28.8 ,command=lambda :self.done(master))
        self.label = ctk.CTkLabel(self, image=master.custom_text("choose destination", bold_font, "white", 12.7, "#727272"), text=None, fg_color="#727272", height=14.4)
        self.frame = ctk.CTkScrollableFrame(self, width=400, height=144)
        self.frame._scrollbar.configure(height=144)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)
        self.columnconfigure(3, weight=0)
        self.columnconfigure(4, weight=1)

        self.label.grid(row=0, column=1, sticky="w", pady=(10, 0), columnspan=3)
        self.frame.grid(row=1, column=1, columnspan=3)
        self.prioritize_btn.grid(row=2, column=1, pady=(10, 0))
        self.delete_btn.grid(row=2, column=2, pady=(10, 0))
        self.done_btn.grid(row=2, column=3, pady=(10, 0))
        self.update()
    
    def update(self):
        for btn in self.priority_btns:
            btn.destroy()
        self.priority_btns = []
        for btn in self.package_btns:
            btn.destroy()
        self.package_btns = []

        for i, p_package in enumerate(self.priority):
            button = ctk.CTkButton(self.frame, text=p_package, corner_radius=None, fg_color="#e0bbbb", text_color="black", hover_color="#6c6969", width=400, height=36, command=lambda i=i: self.select(i, "priority"))
            button.grid(row=i, column=0, pady=(0,2), sticky="we")
            self.priority_btns.append(button)
        num = len(self.priority)
        for i, package in enumerate(self.packages):
            button = ctk.CTkButton(self.frame, text=package, corner_radius=None, fg_color="#dbd4d4", text_color="black", hover_color="#6c6969", width=400, height=36, command=lambda i=i: self.select(i, "package"))
            button.grid(row=num+i, column=0, pady=(0,2), sticky="we")
            self.package_btns.append(button)
        if len(self.selected):
            if self.selected[1] == "priority":
                self.priority_btns[self.selected[0]].configure(fg_color="#898585")
            else:
                self.package_btns[self.selected[0]].configure(fg_color="#898585")
    
    def select(self, index, type):
        self.selected = [index,type]
        self.update()
    
    def prioritize(self):
        if len(self.selected):
            if self.selected[1] == "priority": 
                self.packages.append(self.priority[self.selected[0]])
                self.priority.pop(self.selected[0])
            else: 
                self.priority.append(self.packages[self.selected[0]])
                self.packages.pop(self.selected[0])
            self.selected = []
            self.update()

    def delete(self):
        if len(self.selected):
            if self.selected[1] == "priority": self.priority.pop(self.selected[0])
            else: self.packages.pop(self.selected[0])
            self.selected = []
            self.update()
    
    def done(self, master):
        master.packages = self.packages
        master.priority = self.priority
        self.destroy()

# Run application
if __name__ == "__main__":
    # create app
    app = App()
    
    app.mainloop()
