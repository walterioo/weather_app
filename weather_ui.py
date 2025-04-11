import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
GEO_API = "http://api.openweathermap.org/geo/1.0/direct?"
WEATHER_API = "https://api.openweathermap.org/data/2.5/weather?"

# City class (reuse your existing code)
class City:
    def __init__(self, city, units="metric"):
        self.city = city
        self.units = units

    def get_city_info(self):
        response = requests.get(f"{GEO_API}q={self.city}&limit=1&appid={API_KEY}")
        response.raise_for_status()
        data = response.json()

        if not data or len(data) == 0:
            raise ValueError(f"No city found for {self.city}. Please check the spelling or try a different city.")

        self.city_data = data[0]
        self.city = self.city_data["name"]
        self.lat = self.city_data["lat"]
        self.lon = self.city_data["lon"]

    def get_weather(self):
        response = requests.get(f"{WEATHER_API}lat={self.lat}&lon={self.lon}&units={self.units}&appid={API_KEY}")
        response.raise_for_status()
        self.weather_json = response.json()

        self.temp = self.weather_json["main"]["temp"]
        self.temp_min = self.weather_json["main"]["temp_min"]
        self.temp_max = self.weather_json["main"]["temp_max"]
        self.current_weather = self.weather_json["weather"][0]["main"]

        return {
            "city": self.city,
            "temp": self.temp,
            "temp_min": self.temp_min,
            "temp_max": self.temp_max,
            "current_weather": self.current_weather,
        }

# Function to fetch and display weather
def fetch_weather():
    city_name = city_entry.get().strip()
    units = units_var.get()

    if not city_name:
        messagebox.showerror("Error", "City name cannot be empty!")
        return

    try:
        city_instance = City(city_name, units)
        city_instance.get_city_info()
        weather_data = city_instance.get_weather()

        # Display the weather data
        result_label.config(
            text=(
                f"City: {weather_data['city']}\n"
                f"Temperature: {weather_data['temp']}°{'C' if units == 'metric' else 'F'}\n"
                f"Low: {weather_data['temp_min']}°{'C' if units == 'metric' else 'F'}\n"
                f"High: {weather_data['temp_max']}°{'C' if units == 'metric' else 'F'}\n"
                f"Weather: {weather_data['current_weather']}"
            )
        )
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Weather App")

# City input
tk.Label(root, text="City:").grid(row=0, column=0, padx=10, pady=10)
city_entry = tk.Entry(root, width=30)
city_entry.grid(row=0, column=1, padx=10, pady=10)

# Bind the Enter key to the fetch_weather function
city_entry.bind("<Return>", lambda event: fetch_weather())

# Units selection
tk.Label(root, text="Units:").grid(row=1, column=0, padx=10, pady=10)
units_var = tk.StringVar(value="metric")
tk.Radiobutton(root, text="Metric (°C)", variable=units_var, value="metric").grid(row=1, column=1, sticky="w")
tk.Radiobutton(root, text="Imperial (°F)", variable=units_var, value="imperial").grid(row=2, column=1, sticky="w")

# Fetch weather button
fetch_button = tk.Button(root, text="Get Weather", command=fetch_weather)
fetch_button.grid(row=3, column=0, columnspan=2, pady=10)

# Result display
result_label = tk.Label(root, text="", justify="left")
result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Run the application
root.mainloop()