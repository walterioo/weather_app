import os
from dotenv import load_dotenv
import  requests

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")  # Replace with your actual API key
GEO_API = "http://api.openweathermap.org/geo/1.0/direct?"
WEATHER_API = "https://api.openweathermap.org/data/2.5/weather?"

if not API_KEY:
    raise ValueError("API key is missing. Please set it as an environment variable or in a .env file.")

class City:
    def __init__(self, city, units="metric"):
        self.city = city
        self.units = units
        

    def get_city_info(self): # This method fetches the city information
            try:
                response = requests.get(f"{GEO_API}q={self.city}&limit=1&appid={API_KEY}")
                response.raise_for_status()
                data = response.json()
        
                if not data:
                    raise ValueError("No city found")
            
                city_data = data[0]  
                self.city = city_data["name"]  
                self.lat = city_data["lat"]
                self.lon = city_data["lon"]
                self.get_weather()
                
        
            except requests.exceptions.RequestException:
                print("Error connecting to the API, try again!")
            except (IndexError, KeyError, ValueError) as e:
                print(f"Error: {str(e)}")
          
    def get_weather(self): # This method fetches the weather information
        try:
            response = requests.get(f"{WEATHER_API}lat={self.lat}&lon={self.lon}&units={self.units}&appid={API_KEY}")
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            print("No internet connection")
        except (IndexError, KeyError, ValueError) as e:
                print(f"Error: {str(e)}")

        self.weather_json = response.json()

        self.temp = self.weather_json["main"]["temp"]
        self.temp_min = self.weather_json["main"]["temp_min"]
        self.temp_max = self.weather_json["main"]["temp_max"]
        self.city = self.weather_json["name"]
        self.current_weather = self.weather_json["weather"][0]["main"]

        self.print_weather()
    
    def print_weather(self): # This method prints the weather information
        unit_symbol = "C" if self.units == "metric" else "F"
        print(f"{self.city} current temp is {self.temp} °{unit_symbol}")
        print(f"Today's Low is: {self.temp_min} °{unit_symbol} and High is: {self.temp_max} °{unit_symbol}")
        print(f"Current weather is: {self.current_weather}")        


def weather_init():
    city = input("City: ")
    
    if not city.strip():
        print("City name cannot be empty.")
        weather_init()

    units = input("Units (metric/imperial): ").lower()

    if units not in ["metric", "imperial"]:
        print("Invalid unit. Please enter 'metric' or 'imperial'.")
        weather_init()
    
    city_instance = City(city, units)
    city_instance.get_city_info()


weather_init()