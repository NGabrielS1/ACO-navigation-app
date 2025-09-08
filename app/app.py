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
        self.header_logo = ctk.CTkImage(Image.open(current_path+"/assets/logo_lpb.png"), size=(363, 67.2))
        #fonts
        self.REGULAR = current_path+"/assets/Nexa-ExtraLight.ttf"
        self.BOLD = current_path+"/assets/Nexa-Heavy.ttf"

        #navigation page
        self.header = ctk.CTkFrame(self, height=79.2, width=self.width, fg_color="#f3f2f2", corner_radius=0)
        self.seperator1 = ctk.CTkFrame(self, height=2.4, width=self.width, fg_color="black", corner_radius=0)
        self.inputbar = ctk.CTkFrame(self, height=532.8, width=183, fg_color="#f3f2f2", corner_radius=0)
        self.seperator2 = ctk.CTkFrame(self, height=532.8, width=2.4, fg_color="black", corner_radius=0)
        self.map = ctk.CTkFrame(self, height=532.8, width=506.4, fg_color="green", corner_radius=0)
        self.seperator3 = ctk.CTkFrame(self, height=532.8, width=2.4, fg_color="black", corner_radius=0)
        self.outputbar = ctk.CTkFrame(self, height=532.8, width=183, fg_color="#dbd4d4", corner_radius=0)

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
