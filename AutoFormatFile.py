import os
import shutil
from datetime import datetime

def organize_files_by_date(folder_path):
    # 獲取目標資料夾中的所有檔案
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    for file in files:
        file_path = os.path.join(folder_path, file)
        # 獲取檔案的修改日期
        file_mod_time = os.path.getmtime(file_path)
        # 轉換為日期格式
        file_date = datetime.fromtimestamp(file_mod_time).strftime('%Y-%m-%d')
        # 根據日期建立新的資料夾
        date_folder_path = os.path.join(folder_path, file_date)
        if not os.path.exists(date_folder_path):
            os.makedirs(date_folder_path)
        # 移動檔案到對應的日期資料夾
        shutil.move(file_path, os.path.join(date_folder_path, file))
    
    print("檔案已經按照日期分類完成。")

# 使用者輸入資料夾路徑，並替換反斜杠為正斜杠
folder_path = input("請輸入要整理的資料夾路徑: ").replace("\\", "/")
organize_files_by_date(folder_path)
