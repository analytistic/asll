import pandas as pd
import os

# 设置工作目录
project_root = "D:/asl"
os.chdir(project_root)

# 确认当前工作目录
print("Current working directory:", os.getcwd())

# 指定CSV文件的路径
file_path = 'dataset/lab_1.csv'

# 使用pandas读取CSV文件
data = pd.read_csv(file_path)
print(data)

print(data.columns)