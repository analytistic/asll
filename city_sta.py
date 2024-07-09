import pandas as pd
import os
from geopy.geocoders import Nominatim
import requests
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# 引入数据模块
import sys
sys.path.append('D:/asl/dataset')  # 将根目录添加到系统路径中
import get_data_wx_data


# 设置工作目录
project_root = "D:/asl"
os.chdir(project_root)
# 确认当前工作目录
print("Current working directory:", os.getcwd())

df = get_data_wx_data._get_df()

# 查看数据的列名，确认city列
print(df.columns)

# 高德地图API密钥
api_key = '787091e53a9d8dd0502563fc11ab3fc7'

# 使用Geopy进行地理编码
geolocator = Nominatim(user_agent="geoapiExercises")
def geocode_city(city, api_key):
    url = f'http://api.map.baidu.com/geocoding/v3/?address={city}&output=json&ak={api_key}'
    try:
        response = requests.get(url, timeout=20, verify=False)  # 设置超时时间为10秒
        data = response.json()
        if data['status'] == 0:
            location = data['result']['location']
            print(location)
            return location['lat'], location['lng']
        else:
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error geocoding city {city}: {e}")
        return None, None


# 测试单个城市的地理编码
city_test = '江苏省, 常州市'
lat, lon = geocode_city(city_test, api_key)
print(f"测试城市 {city_test} 的经纬度: {lat}, {lon}")

# 记录未能成功地理编码的城市
# failed_cities = []

# # 为每个城市进行地理编码
# latitudes = []
# longitudes = []
# for city in df['所在城市']:
#     lat, lon = geocode_city(city, api_key)
#     if lat is None or lon is None:
#         failed_cities.append(city)
#     latitudes.append(lat)
#     longitudes.append(lon)
#
# df['latitude'] = latitudes
# df['longitude'] = longitudes

