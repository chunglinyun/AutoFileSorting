# Organize Photos by Date and City
這個專案用於根據照片的拍攝日期和地理位置信息，將照片整理到對應的資料夾中。主要功能包括從照片中提取 EXIF 資料，解析 GPS 資訊，並根據日期和城市名稱分類照片。

## 目錄
- 功能介紹
- 設定文件 `config.json`
- 環境要求
- 安裝
- 使用說明
- 示例
- 常見問題
- 貢獻
- 授權

## 功能介紹
- 從照片中提取 EXIF 資料。
- 解析 GPS 資訊並轉換為經緯度。
- 根據經緯度查詢城市名稱。
- 根據照片拍攝日期和城市名稱分類照片。
- 支援將相同名稱的 RAW 檔案和 JPEG 檔案一起移動。
- 支援人臉識別，將照片按人物分組。
- 支援重複照片檢測，避免存儲多個相同的照片。
- 支援視頻文件和其他媒體類型的整理。
- 提供圖形用戶界面（GUI），便於操作。

## 設定文件
這個文件用來設定是否需要根據城市名稱來分類照片。文件內容如下：
```
{
    "use_city_name": true
}
```
- use_city_name: 布林值，決定是否根據城市名稱來分類照片。如果設置為 true，則會根據照片的GPS信息來查找城市名稱並進行分類；如果設置為 false，則僅根據日期進行分類。
`預設為 flase`
## 環境要求
Python 3.6 或更高版本
需要安裝的 Python 套件：
Pillow
OpenCV
imagehash

## 安裝
1. 克隆這個儲存庫到你的本地機器：

```
git clone https://github.com/yourusername/organize_photos_by_date_and_city.git
2. 進入專案目錄：
```
```
cd organize_photos_by_date_and_city
```
3. 安裝所需的 Python 套件：

```
pip install Pillow
pip install opencv-python
pip install imagehash
```

## 使用說明
1. 運行腳本：

```
python organize_photos.py
```
2. 根據提示輸入要整理的照片資料夾路徑。

3. 程式會自動根據照片的拍攝日期和 GPS 資訊進行分類，並將照片移動到對應的資料夾中。

4. 使用圖形用戶界面（GUI）進行操作：

```
python AutoFormatFile.py
```
5. 在彈出的窗口中選擇要整理的資料夾，程式會自動進行分類。

## 示例
假設有一個名為 photos 的資料夾，其中包含以下照片：

```
photos/
├── img1.jpg
├── img2.jpg
├── img3.ARW
└── img4.CR2
```
運行程式並輸入資料夾路徑後，程式將會根據照片的拍攝日期和 GPS 資訊進行分類，並將照片移動到對應的資料夾中，例如：

```
photos/
├── 2024-06-05_CityName/
│   ├── img1.jpg
│   ├── img3.ARW
│   └── img4.CR2
└── 2024-06-06/
    └── img2.jpg
```
## 常見問題
1. 照片的 EXIF 資料無法讀取？
    - 確保照片是支持 EXIF 資料的格式，例如 JPEG。
    - 確保安裝了 Pillow 庫。
2. 城市名稱無法獲取？

    - 程式中包含了一個模擬的城市名稱查詢函數 get_city_name_nominatim，需要替換成實際實現。
3. RAW 檔案無法識別？

    - 確保 RAW 檔案的副檔名在支援列表中（例如 .nef, .cr2, .arw, .dng, .orf, .rw2）。
4. 如何安裝 OpenCV 和 imagehash 庫？

    - 使用以下命令安裝 OpenCV：
    ```
    pip install opencv-python
    ```
    - 使用以下命令安裝 imagehash：
    ```
    pip install imagehash
    ```

## 貢獻
歡迎提交問題和請求合併（Pull Requests）。在提交請求之前，請確保你的代碼風格和現有項目保持一致，並且已經通過所有測試。

## 授權
此專案採用 MIT 授權條款。詳細資訊請參閱 LICENSE 文件。

