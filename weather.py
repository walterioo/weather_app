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
                
                if not data or len(data) == 0:
                    raise ValueError(f"No city found for {self.city}. Please check the spelling or try a different city.")
                      
                city_data = data[0] # Get the first result
                self.city = city_data["name"]  
                self.lat = city_data["lat"]
                self.lon = city_data["lon"]

                # Check if latitude and longitude are available
                if self.lat is None or self.lon is None:
                    raise ValueError("Latitude or Longitude not found for the city.")
                
            except requests.exceptions.RequestException:
                print("Error connecting to the API, try again!")
            except (IndexError, KeyError, ValueError) as e:
                print(f"Error: {str(e)}")
                weather_init()  # Restart the program if an error occurs
            
            self.get_weather()  # Call the get_weather method to fetch weather data
          
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
    while True:
        print("Welcome to the Weather App! Please enter the city name and units. Type 'exit' to quit.")
        city = input("City: ").strip().lower()
        # Check if the city name is empty or contains non-alphabetic characters
        if city == "exit":
            print("Thanks for use the Weather App!")
            return
        if not city or not all(c.isalpha() or c.isspace() for c in city):
            print("City name invalid. Please enter a valid city name.")
            continue
        break

    while True:
        units = input("Units (metric/imperial): ").lower().strip()
        if units == "exit":
            print("Thanks for use the Weather App!")
            return
        # Check if the units input is valid
        if units not in ["metric", "imperial"]:
            print("Invalid unit. Please enter 'metric' or 'imperial'.")
            continue
        break

    # Create an instance of the City class and call the get_city_info method
    try:
        city_instance = City(city, units)
        city_instance.get_city_info()
    except Exception as e:
        print(f"Error: {str(e)}")
        
# Call the weather_init function to start the program
weather_init()