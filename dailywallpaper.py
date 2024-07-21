import requests
import os
import ctypes
from config import NASAAPI

url = f"https://api.nasa.gov/planetary/apod?api_key={NASAAPI}"
response = requests.get(url)
if response.status_code == 200:
    data = response.json()

current_directory = os.getcwd()
image_url = data['url']
image_file_name = os.path.basename(image_url)
image_file_path = os.path.join(current_directory, image_file_name)

image_response = requests.get(image_url)
if response.status_code == 200:
    with open(image_file_path, "wb") as file:
        file.write(image_response.content)

def set_wallpaper(image_file_path):
    SPI_SETWALLPAPER = 20
    result = ctypes.windll.user32.SystemParametersInfoW(SPI_SETWALLPAPER, 0, image_file_path, 3)
    if result:
        print(f"Wallpaper set successfully: {image_file_path}")
    else:
        print(f"Failed to set wallpaper")

set_wallpaper(image_file_path)