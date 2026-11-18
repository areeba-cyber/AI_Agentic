import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):

    if not city or not city.strip():
        raise ValueError("City name cannot be empty.")

    if not API_KEY:
        raise RuntimeError("API key is missing.")

    params = {
        "q": city.strip(),
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if not isinstance(data, dict):
            raise ValueError("Invalid API response.")

        return data

    except requests.exceptions.Timeout:
        raise RuntimeError("Request timed out.")

    except requests.exceptions.HTTPError as error:
        raise RuntimeError(
            f"Weather API returned an HTTP error: {error}"
        )

    except requests.exceptions.ConnectionError:
        raise RuntimeError("Please check your internet connection.")

    except requests.exceptions.RequestException as error:
        raise RuntimeError(f"API request failed: {error}")

    except ValueError as error:
        raise RuntimeError(f"Invalid JSON response: {error}")

def display_weather(data):

    city = data["name"]

    temperature = data["main"]["temp"]

    humidity = data["main"]["humidity"]

    condition = data["weather"][0]["description"]

    wind_speed = data["wind"]["speed"]

    print("\n------ WEATHER REPORT ------")

    print(f"City: {city}")
    print(f"Temperature: {temperature}°C")
    print(f"Humidity: {humidity}%")
    print(f"Condition: {condition}")
    print(f"Wind Speed: {wind_speed} m/s")

    print("----------------------------")

if __name__ == "__main__":

    city = input("Enter city name: ")

    try:
        weather_data = get_weather(city)

        display_weather(weather_data)

    except (ValueError, RuntimeError) as error:
        print(f"Error: {error}")