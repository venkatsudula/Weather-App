import tkinter as tk


import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap
from ttkbootstrap import Style
def get_weather(city):
    API_key = "35e40c737d0ecdc59aafd48c2e1bf9e2"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    
    try:
        res = requests.get(url)
        res.raise_for_status()  # Raise an error for bad responses (e.g., 404)
        weather = res.json()
        
        icon_id = weather['weather'][0]['icon']
        temperature = weather['main']['temp'] - 273.15  # Convert Kelvin to Celsius
        description = weather['weather'][0]['description']
        city = weather['name']
        country = weather['sys']['country']
        icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"

        return (icon_url, temperature, description, city, country)

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch weather data.\n{e}")
        return None

def search():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Warning", "Please enter a city name!")
        return

    result = get_weather(city)
    if result is None:
        return
    
    icon_url, temperature, description, city, country = result
    
    location_label.config(text=f"{city}, {country}")
    
    try:
        image = Image.open(requests.get(icon_url, stream=True).raw)
        icon = ImageTk.PhotoImage(image)
        icon_label.configure(image=icon)
        icon_label.image = icon
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load weather icon.\n{e}")

    temperature_label.configure(text=f"Temperature: {temperature:.2f}°C")
    description_label.configure(text=f"Description: {description.capitalize()}")

# Create the main application window
style = Style(theme="morph")
root = style.master
root.title("Weather App")
root.geometry("400x400")

# City entry field
city_entry = tk.Entry(root, font=("Helvetica", 18))
city_entry.pack(pady=10)

# Search button
search_button = tk.Button(root, text="Search", command=search)
search_button.pack(pady=10)

# Labels for displaying weather information
location_label = tk.Label(root, font=("Helvetica", 25))
location_label.pack(pady=20)

icon_label = tk.Label(root)
icon_label.pack()

temperature_label = tk.Label(root, font=("Helvetica", 20))
temperature_label.pack()

description_label = tk.Label(root, font=("Helvetica", 20))
description_label.pack()

# Start the Tkinter event loop
root.mainloop()
