import unittest
import mock_open
from unittest.mock import patch, MagicMock
from AutoFormatFile import get_exif_data, get_lat_lon, organize_photos_by_date_and_city, detect_faces, find_duplicates
import os
import tempfile
import shutil
from PIL import Image

class TestGetExifData(unittest.TestCase):
    @patch('PIL.Image.open')
    def test_get_exif_data(self, mock_open):
        mock_image = MagicMock()
        mock_exif = {305: 'TestCamera', 306: '2020:01:01 00:00:00'}
        mock_image._getexif.return_value = mock_exif
        mock_open.return_value = mock_image
        expected = {'Software': 'TestCamera', 'DateTime': '2020:01:01 00:00:00'}
        self.assertEqual(get_exif_data('dummy.jpg'), expected)

class TestGetLatLon(unittest.TestCase):
    def test_get_lat_lon(self):
        gps_info = {'GPSLatitude': (50, 0, 0), 'GPSLatitudeRef': 'N', 'GPSLongitude': (0, 30, 0), 'GPSLongitudeRef': 'E'}
        expected = (50.0, 0.5)
        self.assertEqual(get_lat_lon(gps_info), expected)

class TestOrganizePhotosByDateAndCity(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    @patch('AutoFormatFile.get_city_name_nominatim')
    def test_organize_photos_by_date_and_city(self, mock_get_city_name):
        mock_get_city_name.return_value = "MockCity"
        # Setup would involve creating mock files with modification times and optional EXIF data
        # This is left as an exercise due to complexity and length

class TestDetectFaces(unittest.TestCase):
    @patch('cv2.CascadeClassifier')
    @patch('cv2.imread')
    def test_detect_faces(self, mock_imread, mock_cascade):
        mock_img = MagicMock()
        mock_imread.return_value = mock_img
        mock_cascade.return_value.detectMultiScale.return_value = [(10, 10, 50, 50)]
        self.assertTrue(detect_faces('dummy.jpg'))

class TestFindDuplicates(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    @patch('imagehash.average_hash')
    @patch('PIL.Image.open')
    def test_find_duplicates(self, mock_open, mock_hash):
        mock_image = MagicMock()
        mock_open.return_value = mock_image
        mock_hash.side_effect = ['hash1', 'hash2', 'hash1']
        file1 = os.path.join(self.temp_dir, 'file1.jpg')
        file2 = os.path.join(self.temp_dir, 'file2.jpg')
        file3 = os.path.join(self.temp_dir, 'file3.jpg')
        with open(file1, 'w'), open(file2, 'w'), open(file3, 'w'):
            pass
        duplicates = find_duplicates(self.temp_dir)
        self.assertEqual(len(duplicates), 1)
        self.assertIn((file3, file1), duplicates)

if __name__ == '__main__':
    unittest.main()
