import os
import shutil
import json
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import cv2
import numpy as np
import imagehash
from tkinter import Tk, Label, Button, filedialog

from GetCityName import get_city_name_nominatim

def get_exif_data(image_path):
    """Extract EXIF data from an image."""
    exif_data = {}
    try:
        img = Image.open(image_path)
        info = img._getexif()
        if info:
            for tag, value in info.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == "GPSInfo":
                    gps_data = {}
                    for t in value:
                        sub_tag_name = GPSTAGS.get(t, t)
                        gps_data[sub_tag_name] = value[t]
                    exif_data[tag_name] = gps_data
                else:
                    exif_data[tag_name] = value
    except Exception as e:
        print(f"Error reading EXIF data from {image_path}: {e}")
    return exif_data

def get_lat_lon(gps_info):
    """Convert the GPS coordinates into latitude and longitude."""
    def convert_to_degrees(value):
        d = float(value[0])
        m = float(value[1]) / 60.0
        s = float(value[2]) / 3600.0
        return d + m + s

    lat = convert_to_degrees(gps_info['GPSLatitude'])
    if gps_info['GPSLatitudeRef'] == 'S':
        lat = -lat

    lon = convert_to_degrees(gps_info['GPSLongitude'])
    if gps_info['GPSLongitudeRef'] == 'W':
        lon = -lon

    return lat, lon

def check_and_create_config(config_file_path):
    """Check if the config file exists, and create it with default values if it does not."""
    if not os.path.exists(config_file_path):
        default_config = {
            "use_city_name": True,
            "detect_faces": False
        }
        with open(config_file_path, 'w') as config_file:
            json.dump(default_config, config_file)
        print(f"配置文件 '{config_file_path}' 不存在，已創建默認配置文件。")
    # 讀取配置文件
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
    return config

def detect_faces(image_path):
    """Detect faces in an image using OpenCV."""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    return len(faces) > 0

def find_duplicates(folder_path):
    """Find duplicate photos in a folder using image hashing."""
    hashes = {}
    duplicates = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                img = Image.open(file_path)
                img_hash = imagehash.average_hash(img)
                if img_hash in hashes:
                    duplicates.append((file_path, hashes[img_hash]))
                else:
                    hashes[img_hash] = file_path
    return duplicates

def organize_photos_by_date_and_city(folder_path):

    # 讀取配置文件
    config_file_path = 'config.json'
    config = check_and_create_config(config_file_path)
    
    use_city_name = config.get("use_city_name", False)
    detect_faces_enabled = config.get("detect_faces", False)

    # 獲取目標資料夾中的所有檔案
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    city_cache = {}

    for file in files:
        file_path = os.path.join(folder_path, file)
        exif_data = get_exif_data(file_path)
        file_date = None
        city_name = None
        date_city_folder_path = None

        # 獲取檔案的修改日期
        file_mod_time = os.path.getmtime(file_path)
        file_date = datetime.fromtimestamp(file_mod_time).strftime('%Y-%m-%d')

        if use_city_name and 'GPSInfo' in exif_data:
            gps_info = exif_data['GPSInfo']
            lat, lon = get_lat_lon(gps_info)
            if (lat, lon) in city_cache:
                city_name = city_cache[(lat, lon)]
            else:
                city_name = get_city_name_nominatim(lat, lon)
                city_cache[(lat, lon)] = city_name

        # 根據日期和城市名稱建立新的資料夾
        if city_name:
            date_city_folder_path = os.path.join(folder_path, f"{file_date}_{city_name}")
        else:
            date_city_folder_path = os.path.join(folder_path, file_date)

        if not os.path.exists(date_city_folder_path):
            os.makedirs(date_city_folder_path)
        # 移動檔案到對應的日期/城市資料夾
        shutil.move(file_path, os.path.join(date_city_folder_path, file))

    print("照片已經按照日期和城市名稱分類完成。")

    # Detect faces and find duplicates
    if detect_faces_enabled:
        for file in files:
            file_path = os.path.join(folder_path, file)
            if detect_faces(file_path):
                print(f"Detected faces in {file}")
    duplicates = find_duplicates(folder_path)
    if duplicates:
        print("Duplicate photos found:")
        for dup in duplicates:
            print(f"Duplicate: {dup[0]} and {dup[1]}")

def organize_videos_by_date_and_city(folder_path):
    """Organize video files by date and city."""
    # 獲取目標資料夾中的所有檔案
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    city_cache = {}

    for file in files:
        file_path = os.path.join(folder_path, file)
        file_date = None
        city_name = None
        date_city_folder_path = None

        # 獲取檔案的修改日期
        file_mod_time = os.path.getmtime(file_path)
        file_date = datetime.fromtimestamp(file_mod_time).strftime('%Y-%m-%d')

        if use_city_name:
            # Use a placeholder for city name as videos do not have EXIF data
            city_name = "UnknownCity"

        # 根據日期和城市名稱建立新的資料夾
        if city_name:
            date_city_folder_path = os.path.join(folder_path, f"{file_date}_{city_name}")
        else:
            date_city_folder_path = os.path.join(folder_path, file_date)

        if not os.path.exists(date_city_folder_path):
            os.makedirs(date_city_folder_path)
        # 移動檔案到對應的日期/城市資料夾
        shutil.move(file_path, os.path.join(date_city_folder_path, file))

    print("視頻已經按照日期和城市名稱分類完成。")

def create_gui():
    """Create a graphical user interface using Tkinter."""
    def select_folder():
        folder_path = filedialog.askdirectory()
        if folder_path:
            organize_photos_by_date_and_city(folder_path)
            organize_videos_by_date_and_city(folder_path)

    root = Tk()
    root.title("Organize Photos and Videos")
    label = Label(root, text="Select a folder to organize:")
    label.pack(pady=10)
    button = Button(root, text="Select Folder", command=select_folder)
    button.pack(pady=10)
    root.mainloop()

# 使用者輸入資料夾路徑，並替換反斜杠為正斜杠
folder_path = input("請輸入要整理的資料夾路徑: ").replace("\\", "/")
organize_photos_by_date_and_city(folder_path)
organize_videos_by_date_and_city(folder_path)

# 等待用戶輸入，以防視窗立即關閉
input("Press Enter to exit...")

# Create GUI
create_gui()
