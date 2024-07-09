import pandas as pd
import os

# 设置工作目录
project_root = "D:/asl"
os.chdir(project_root)

# 确认当前工作目录
print("Current working directory:", os.getcwd())




# 使用pandas读取CSV文件


def get_data():
    # 指定CSV文件的路径
    file_path = 'dataset/lab_1.csv'
    data = pd.read_csv(file_path)
    return data




# # 查看数据的列名，确认city列
# print(data.columns)
# column_name = '发病前长期居住地'

# 根据城市名称取得地理位置编码
# 使用Geopy进行地理编码
# geolocator = Nominatim(user_agent="geoapiExercises")

# def geocode_city(city):
#     try:
#         location = geolocator.geocode(city + ", China")
#         return location.latitude, location.longitude
#     except:
#         return None, None
#
# df['latitude'], df['longitude'] = zip(*df['city'].apply(geocode_city))



# 继续筛选字符数少于5的数据

# # 筛选第17列中包含数字、‘号’或‘室’的行
# filtered_data = data[data[column_name].str.contains(r'\d|号|室|一|二|三|四|五|六|七|八|九|十', na=False)]
#
# # 筛选掉第17列中字符数少于5个的行
# filtered_data = filtered_data[filtered_data[column_name].str.len() >= 7]
# # 筛除只精确到市的信息
# # filtered_data = filtered_data[~filtered_data[column_name].str.endswith('市', na=False)]
#
# filtered_data = filtered_data.iloc[:, [ 1, 17]]

# 显示剔除后的数据

# # 设置pandas显示选项
# print('筛选后的数据',filtered_data)
# print(filtered_data.shape)

