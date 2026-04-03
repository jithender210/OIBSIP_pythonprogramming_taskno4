import tkinter as tk
from tkinter import messagebox
import requests
from io import BytesIO
import numpy as np
from PIL import Image, ImageTk
API_KEY = "your_api_key_here"  # Replace with your OpenWeatherMap API key
def get_weather():
    city=city_var.get()
    
    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return
    units="metric" if unit.get()=="Celsius" else "imperial"
    
    url=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={units}"
    responce=requests.get(url)
    
    try:
        if responce.status_code!=200:
            messagebox.showerror("Error", "City not found or API error.")
            return
        if responce.status_code==200:
            weather_data=responce.json()
        
            temp=round(weather_data["main"]["temp"],2)
            weather=weather_data["weather"][0]["description"]
            wind_speed=weather_data["wind"]["speed"]

            temp_Label.config(text=f"Temperature: {temp}°{'C' if units=='metric' else 'F'}")
            weather_Label.config(text=f"Weather: {weather}")
            wind_speed_lb.config(text=f"Wind Speed: {wind_speed:.2f} m/s")

            img_code=weather_data["weather"][0]["icon"]
            img_url=f"http://openweathermap.org/img/wn/{img_code}.png"
            img_data=requests.get(img_url, stream=True).content
            img=Image.open(BytesIO(img_data))
            img=img.resize((100,100))
            img=ImageTk.PhotoImage(img)
            img_lb.config(image=img)
            img_lb.image=img
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


#-------  GUI setup  --------
root = tk.Tk()
root.title("Weather App")
root.geometry("500x500")
tk.Label(root, text="CITY",font=("Arial", 20)).pack(pady=10)
city_var = tk.StringVar()
entry=tk.Entry(root,font=("Arial", 12),width=30, textvariable=city_var)
entry.pack(pady=5)
unit=tk.StringVar(value="Celsius")
tk.Radiobutton(root,text="Celsius",value="Celsius",variable=unit,font=("Arial", 12)).pack(pady=5)
tk.Radiobutton(root,text="Fahrenheit",value="Fahrenheit",variable=unit,font=("Arial", 12)).pack(pady=5)
tk.Button(root, text="Get Weather",font=("Arial", 12),bg="#87CEEB", command=lambda: get_weather()).pack(pady=10)

#-------  results display  --------
temp_Label=tk.Label(root, text="",font=("Arial", 12))
temp_Label.pack(pady=10)
weather_Label=tk.Label(root, text="",font=("Arial", 12))
weather_Label.pack(pady=10)
wind_speed_lb=tk.Label(root, text="",font=("Arial", 12))
wind_speed_lb.pack(pady=10)

img_lb=tk.Label(root,bg="#87CEEB")
img_lb.pack(pady=10)
root.mainloop()
