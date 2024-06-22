import requests

def get_city_name_nominatim(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'address' in data and 'city' in data['address']:
            return data['address']['city']
    return None

# 示例使用
lat, lon = 37.7749, -122.4194
city_name = get_city_name_nominatim(lat, lon)
print(city_name)
