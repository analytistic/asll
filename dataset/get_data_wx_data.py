import pandas as pd
import os

# 设置工作目录
project_root = "D:/asl"
os.chdir(project_root)

# 确认当前工作目录
print("Current working directory:", os.getcwd())


# 使用pandas读取CSV文件
def _get_df():
    file_path = 'dataset/wx_data.csv'
    df = pd.read_csv(file_path)
    return df


# 查看数据的列名，确认city列
df = _get_df()
print(df.columns)



# 显示前5行数据
# print(df.head())

# 假设第八列名称为 'Column8'
# column_name = df.columns[7]  # 获取第八列的名称·
# print(column_name)


# 筛选第八列最后一个字符为 '市' 的行
# filtered_data = df[df[column_name].str.endswith('市', na=False)]
#
# filtered_data = df[~data[column_name].str.endswith('市', na=False)]
#
# 保存剔除后的数据到新的CSV文件
# output_file_path = 'dataset/city_none_data.csv'  # 指定保存路径（Windows）
# filtered_data.to_csv(output_file_path, index=False, encoding='utf-8-sig')
#
# 显示剔除后的数据
# print('筛选后的数据',filtered_data)




