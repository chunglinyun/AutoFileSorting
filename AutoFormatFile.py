import os
import shutil
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

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

def organize_photos_by_date_and_city(folder_path):
    # 獲取目標資料夾中的所有檔案
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    city_cache = {}
    move_operations = []

    # 檔案類型過濾，只處理 JPG 檔案
    image_files = [f for f in files if f.lower().endswith('.jpg') or f.lower().endswith('.jpeg')]

    for file in image_files:
        file_path = os.path.join(folder_path, file)
        exif_data = get_exif_data(file_path)
        file_date = None
        city_name = None
        date_city_folder_path = None

        # 獲取檔案的修改日期
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
            date_city_folder_path = os.path.join(folder_path, file_date)

        if not os.path.exists(date_city_folder_path):
            os.makedirs(date_city_folder_path)

        # 記錄移動操作
        move_operations.append((file_path, os.path.join(date_city_folder_path, file)))

        # 檢查是否存在相同名稱的RAW檔
        raw_file_extensions = ['.nef', '.cr2', '.arw', '.dng', '.orf', '.rw2']
        file_name, file_ext = os.path.splitext(file)
        for ext in raw_file_extensions:
            raw_file = file_name + ext
            raw_file_path = os.path.join(folder_path, raw_file)
            if os.path.exists(raw_file_path):
                move_operations.append((raw_file_path, os.path.join(date_city_folder_path, raw_file)))

    # 執行移動操作
    for src, dst in move_operations:
        try:
            shutil.move(src, dst)
        except Exception as e:
            print(f"Error moving file {src} to {dst}: {e}")

    print("照片已經按照日期和城市名稱分類完成。")

# 使用者輸入資料夾路徑，並替換反斜杠為正斜杠
folder_path = input("請輸入要整理的資料夾路徑: ").replace("\\", "/")
organize_photos_by_date_and_city(folder_path)
