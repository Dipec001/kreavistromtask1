import requests
import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
import config

API_KEY = config.MY_API_KEY


# Step 1: API Call to Get Weather Data
def get_weather_data(api_key, location):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data


# Step 2: Parse JSON Data
def parse_weather_data(data):
    # Extract relevant weather information from the JSON data
    weather_description = data['weather'][0]['description']
    temperature = data['main']['temp']
    icon_name = data['weather'][0]['main'].lower()
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    return weather_description, temperature, icon_name, pressure,humidity


# Step 3: Create a GUI using tkinter
def create_weather_app():
    app = tk.Tk()
    app.title("Weather App")
    app.geometry("600x400")

    location_label = tk.Label(app, text="Enter Location:")
    location_label.pack()

    location_entry = tk.Entry(app)
    location_entry.pack()

    # Create label for displaying current time
    time_label = tk.Label(app, text="", font=("Helvetica", 16))
    time_label.pack()

    def update_weather():
        location = location_entry.get()
        try:
            weather_data = get_weather_data(api_key, location)
            description, temperature, icon_name, pressure, humidity = parse_weather_data(weather_data)

            # Update GUI elements with weather information
            weather_label.config(text=f"Weather: {description}")
            temperature_label.config(text=f"Temperature: {temperature}°C")
            pressure_label.config(text=f"Pressure: {pressure}hpa")
            humidity_label.config(text=f"Humidity: {humidity}%")

            # Replace the 'icon_path' line in the 'update_weather' function with this code
            icon_code = weather_data['weather'][0]['icon']
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
            icon_data = requests.get(icon_url, stream=True)
            if icon_data.status_code == 200:
                with open("weather_icon.png", "wb") as icon_file:
                    for chunk in icon_data.iter_content(128):
                        icon_file.write(chunk)
                weather_icon = Image.open("weather_icon.png")
                weather_icon = ImageTk.PhotoImage(weather_icon)
                icon_label.config(image=weather_icon)
                icon_label.image = weather_icon

            # Update the current time label
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            time_label.config(text=f"Current Time: {current_time}")
        except requests.exceptions.RequestException as e:
            # Handle API request errors (e.g., connection error)
            print(f"API Request Error: {e}")
        except KeyError as e:
            # Handle JSON parsing errors (e.g., missing data)
            print(f"JSON Parsing Error: {e}")
        except Exception as e:
            # Handle other unexpected errors
            print(f"An unexpected error occurred: {e}")

    update_button = tk.Button(app, text="Update Weather", command=update_weather)
    update_button.pack()

    weather_label = tk.Label(app, text="")
    weather_label.pack()

    temperature_label = tk.Label(app, text="")
    temperature_label.pack()

    empty_image = ImageTk.PhotoImage(Image.new("RGB", (1, 1)))  # Create an empty ImageTk
    icon_label = tk.Label(app, image=empty_image)
    icon_label.image = empty_image  # Assign it to the label
    icon_label.pack()

    pressure_label = tk.Label(app, text="")
    pressure_label.pack()

    humidity_label = tk.Label(app, text="")
    humidity_label.pack()

    app.mainloop()


api_key = API_KEY

# My APP
create_weather_app()
