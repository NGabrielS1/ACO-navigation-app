import os
import time
import math
import random
import numpy as np
import pandas as pd
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

    start = None
    Priority = []
    Packages = []
    End = None

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
        self.input_btn = ctk.CTkButton(self.inputbar, image=self.custom_text("input dests", self.BOLD, "#ffffff", 19.8, "#5170ff"), text=None, fg_color="#5170ff", hover_color="#5170ff", width=148.2, height=35.4, corner_radius=28.8 ,command=None)
        self.check_btn = ctk.CTkButton(self.inputbar, image=self.custom_text("check dests", self.BOLD, "#ffffff", 19.8, "#5170ff"), text=None, fg_color="#5170ff", hover_color="#5170ff", width=148.2, height=35.4, corner_radius=28.8 ,command=None)

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

# Run application
if __name__ == "__main__":
    # create app
    app = App()
    
    app.mainloop()
