import os
import shutil
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif_data(image):
    """Extract EXIF data from an image."""
    exif_data = {}
    try:
        img = Image.open(image)
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
        print(f"Error reading EXIF data from {image}: {e}")
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

def get_city_name_nominatim(lat, lon):
    """Mock function to simulate city name lookup."""
    # Replace this with your actual implementation
    return "CityName"

def organize_photos_by_date_and_city(folder_path):
    # 取得目標資料夾中的所有檔案
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    city_cache = {}

    for file in files:
        file_path = os.path.join(folder_path, file)
        exif_data = get_exif_data(file_path)
        file_date = None
        city_name = None

        # 取得檔案的修改日期
        file_mod_time = os.path.getmtime(file_path)
        file_date = datetime.fromtimestamp(file_mod_time).strftime('%Y-%m-%d')

        if 'GPSInfo' in exif_data:
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
            date_folder_path = os.path.join(folder_path, file_date)

        if not os.path.exists(date_city_folder_path):
            os.makedirs(date_city_folder_path)
        # 移動檔案到對應的日期/城市資料夾
        shutil.move(file_path, os.path.join(date_city_folder_path, file))

    print("照片已經按照日期和城市名稱分類完成。")

# 使用者輸入資料夾路徑，並替換反斜杠為正斜杠
folder_path = input("請輸入要整理的資料夾路徑: ").replace("\\", "/")
organize_photos_by_date_and_city(folder_path)
