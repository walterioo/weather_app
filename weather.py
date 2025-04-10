import  requests

API_KEY = "6e9ac994f4847707ae8e96f675fd2eec"

class City:
    def __init__(self, name, units="metric"):
        self.name = name
        self.units = units
        

    def get_city_info(self):
            try:
                response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={self.name}&limit=1&appid={API_KEY}")
                response.raise_for_status()
                data = response.json()
        
                if not data:
                    raise ValueError("No city found")
            
                city_data = data[0]  # Will raise IndexError if empty
                self.city = city_data["name"]  # Will raise KeyError if missing
                self.lat = city_data["lat"]
                self.lon = city_data["lon"]
                self.get_weather()
                
        
            except requests.exceptions.RequestException:
                print("Error connecting to the API, try again!")
            except (IndexError, KeyError, ValueError) as e:
                print(f"Error: {str(e)}")
          
    def get_weather(self):
        try:
            response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&units={self.units}&appid={API_KEY}")
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            print("No internet connection")
        except:
            print("other error")

        self.weather_json = response.json()

        self.temp = self.weather_json["main"]["temp"]
        self.temp_min = self.weather_json["main"]["temp_min"]
        self.temp_max = self.weather_json["main"]["temp_max"]
        self.city = self.weather_json["name"]
        self.current_weather = self.weather_json["weather"][0]["main"]

        self.print_weather()
    
    def print_weather(self):
        if self.units == "metric":
            unit_symbol = "C"
        if self.units == "imperial":
            unit_symbol = "F"
        print(f"{self.city} current temp is {self.temp} °{unit_symbol}")
        print(f"Today's Low is: {self.temp_min} °{unit_symbol} and High is: {self.temp_max} °{unit_symbol}")
        print(f"Current weather is: {self.current_weather}")        

city = input("City: ")

search_city = City(city)
search_city.get_city_info()
