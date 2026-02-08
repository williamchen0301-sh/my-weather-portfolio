import tkinter as tk
from tkinter import messagebox
import requests
import time
import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

def get_weather(city="Pittsburgh"):
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        messagebox.showerror("Error", "API Key not found in .env file.")
        return None

    # Weatherstack API Endpoint
    # Note: The free plan only supports HTTP, not HTTPS.
    base_url = "http://api.weatherstack.com/current"
    
    params = {
        'access_key': api_key,
        'query': city,
        'units': 'f'  # 'f' for Fahrenheit, 'm' for Metric, 's' for Scientific
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        # Weatherstack returns a "success": false field if there is an error
        if 'success' in data and data['success'] is False:
            error_msg = data['error']['info']
            messagebox.showerror("API Error", f"Error: {error_msg}")
            return None
            
        return data
    except Exception as e:
        messagebox.showerror("Connection Error", f"Could not connect: {e}")
        return None

def update_display():
    city = city_entry.get()
    if not city:
        city = "Pittsburgh"

    weather_data = get_weather(city)
    
    if weather_data:
        try:
            # --- NEW PARSING LOGIC FOR WEATHERSTACK ---
            current = weather_data['current']
            location = weather_data['location']

            temp = current['temperature']
            feels_like = current['feelslike']
            # Weatherstack returns a list of descriptions
            condition = current['weather_descriptions'][0] if current['weather_descriptions'] else "Unknown"
            humidity = current['humidity']
            wind_speed = current['wind_speed']
            city_name = location['name']
            
            # Update GUI Labels
            lbl_city.config(text=f"{city_name}")
            lbl_temp.config(text=f"{temp}°F")
            lbl_desc.config(text=f"{condition}")
            lbl_details.config(text=f"Feels like: {feels_like}°F | Humidity: {humidity}% | Wind: {wind_speed} mph")
            
            # Update status
            current_time = time.strftime("%I:%M %p")
            lbl_status.config(text=f"Last updated: {current_time} (Weatherstack)")
            
        except KeyError as e:
            messagebox.showerror("Data Error", f"Unexpected data format: {e}")

# --- GUI Setup (Same as before) ---
root = tk.Tk()
root.title("Pittsburgh Weather (Weatherstack)")
root.geometry("400x450")
root.configure(bg="#f0f4f8")

tk.Label(root, text="Weather App", font=("Helvetica", 12, "bold"), bg="#f0f4f8", fg="#333").pack(pady=10)

control_frame = tk.Frame(root, bg="#f0f4f8")
control_frame.pack(pady=5)

city_entry = tk.Entry(control_frame, font=("Helvetica", 14), width=15, justify='center')
city_entry.insert(0, "Pittsburgh")
city_entry.pack(side=tk.LEFT, padx=5)

search_btn = tk.Button(control_frame, text="Search", command=update_display, bg="#007bff", fg="white", font=("Helvetica", 10, "bold"))
search_btn.pack(side=tk.LEFT, padx=5)

display_frame = tk.Frame(root, bg="white", bd=2, relief="groove")
display_frame.pack(pady=20, padx=20, fill="both", expand=True)

lbl_city = tk.Label(display_frame, text="--", font=("Helvetica", 24, "bold"), bg="white", fg="#333")
lbl_city.pack(pady=(20, 5))

lbl_temp = tk.Label(display_frame, text="--°F", font=("Helvetica", 48, "bold"), bg="white", fg="#007bff")
lbl_temp.pack(pady=5)

lbl_desc = tk.Label(display_frame, text="--", font=("Helvetica", 16, "italic"), bg="white", fg="#666")
lbl_desc.pack(pady=5)

lbl_details = tk.Label(display_frame, text="--", font=("Helvetica", 10), bg="white", fg="#555")
lbl_details.pack(pady=(10, 20))

lbl_status = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#dfe6e9", font=("Arial", 8))
lbl_status.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()