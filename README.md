Organize Photos by Date and City
這個專案用於根據照片的拍攝日期和地理位置信息，將照片整理到對應的資料夾中。主要功能包括從照片中提取 EXIF 資料，解析 GPS 資訊，並根據日期和城市名稱分類照片。

目錄
功能介紹
環境要求
安裝
使用說明
示例
常見問題
貢獻
授權
功能介紹
從照片中提取 EXIF 資料。
解析 GPS 資訊並轉換為經緯度。
根據經緯度查詢城市名稱。
根據照片拍攝日期和城市名稱分類照片。
支援將相同名稱的 RAW 檔案和 JPEG 檔案一起移動。
環境要求
Python 3.6 或更高版本
需要安裝的 Python 套件：
Pillow
安裝
克隆這個儲存庫到你的本地機器：

bash
Copy code
git clone https://github.com/yourusername/organize_photos_by_date_and_city.git
進入專案目錄：

bash
Copy code
cd organize_photos_by_date_and_city
安裝所需的 Python 套件：

bash
Copy code
pip install Pillow
使用說明
運行腳本：

bash
Copy code
python organize_photos.py
根據提示輸入要整理的照片資料夾路徑。

程式會自動根據照片的拍攝日期和 GPS 資訊進行分類，並將照片移動到對應的資料夾中。

示例
假設有一個名為 photos 的資料夾，其中包含以下照片：

Copy code
photos/
├── img1.jpg
├── img2.jpg
├── img3.ARW
└── img4.CR2
運行程式並輸入資料夾路徑後，程式將會根據照片的拍攝日期和 GPS 資訊進行分類，並將照片移動到對應的資料夾中，例如：

yaml
Copy code
photos/
├── 2024-06-05_CityName/
│   ├── img1.jpg
│   ├── img3.ARW
│   └── img4.CR2
└── 2024-06-06/
    └── img2.jpg
常見問題
照片的 EXIF 資料無法讀取？

確保照片是支持 EXIF 資料的格式，例如 JPEG。
確保安裝了 Pillow 庫。
城市名稱無法獲取？

程式中包含了一個模擬的城市名稱查詢函數 get_city_name_nominatim，需要替換成實際實現。
RAW 檔案無法識別？

確保 RAW 檔案的副檔名在支援列表中（例如 .nef, .cr2, .arw, .dng, .orf, .rw2）。
貢獻
歡迎提交問題和請求合併（Pull Requests）。在提交請求之前，請確保你的代碼風格和現有項目保持一致，並且已經通過所有測試。

授權
此專案採用 MIT 授權條款。詳細資訊請參閱 LICENSE 文件。

