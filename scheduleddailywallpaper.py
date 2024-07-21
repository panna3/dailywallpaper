import requests
import ctypes
import os
import schedule
import time
from datetime import datetime
from config import NASAAPI

# Function to download image
def download_image(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, 'wb') as file:
            file.write(response.content)
        print(f"Image downloaded successfully: {path}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

# Function to set wallpaper
def set_wallpaper(image_path):
    SPI_SETDESKWALLPAPER = 20
    result = ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)
    if result:
        print(f"Wallpaper set successfully: {image_path}")
    else:
        print("Failed to set wallpaper")

# Function to get the NASA APOD image and set as wallpaper
def update_wallpaper():
    # URL for the NASA APOD API
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASAAPI}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        # Extract the image URL
        image_url = data['url']
        
        # Get the current working directory
        current_directory = os.getcwd()
        
        # Define the image file path
        image_file_name = os.path.basename(image_url)
        image_file_path = os.path.join(current_directory, image_file_name)
        
        # Download the image
        download_image(image_url, image_file_path)
        
        # Set the wallpaper
        set_wallpaper(image_file_path)
    else:
        print(f"Failed to fetch APOD data. Status code: {response.status_code}")

# Schedule the task to run every day at a specific time
schedule.every().day.at("11:55").do(update_wallpaper)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
