import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import re
import statsmodels.api as sm

# 设置工作目录
project_root = "D:/asl"
os.chdir(project_root)

# 引入get_data_lab_1模块
import sys
sys.path.append('D:/asl/dataset')  # 将根目录添加到系统路径中
import get_data_lab_1

# 获取数据
data = get_data_lab_1.get_data()

# 确保系统中有中文字体，并设置为 SimHei
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决坐标轴负号显示问题

# 查看数据基本信息
print(data.info())

# # 查看数据的统计描述
# print(data.describe())
#
# # 检查数据的前几行
# print(data.head())
#
# # 检查缺失值
# print(data.isnull().sum())


# 替换column的信息
data['性别'] = data['性别'].replace({'男': 'M', '女': 'W'})
# 检查 '性别' 列的数据类型和值
print(data['性别'].dtype)
print(data['性别'].unique())
# 确保 '性别' 列中没有缺失值
data = data.dropna(subset=['性别'])

# # 直方图
# sns.histplot(data['近三个月AR分数平均月变化'], kde= True)
# plt.title('Age vs Income')
# plt.show()

# 数据清洗
# 定义一个函数来提取数值部分
def extract_numeric(value):
    match = re.search(r'(\d+(\.\d+)?)', str(value))
    if match:
        return float(match.group(1))
    return None

# 指定要绘制的变量
variables_to_plot = ['近一年AR分数平均月变化', '近三个月AR分数平均月变化', '发病前体重', '当前体重（kg）', '身高（厘米）']

for var in variables_to_plot:
    data[var] = data[var].apply(extract_numeric)
    data[var] = pd.to_numeric(data[var], errors='coerce')

# 删除包含非数值类型（转换为NaN）的行
data = data.dropna(subset=variables_to_plot)

# 指定要绘制的变量
data['体重差值（kg）'] = data['当前体重（kg）'] - data['发病前体重']
variables_to_plot = ['近一年AR分数平均月变化', '近三个月AR分数平均月变化', '发病前体重', '当前体重（kg）', '体重差值（kg）', '身高（厘米）']

# 设置显示选项
pd.set_option('display.max_rows', None)  # 显示所有行
pd.set_option('display.max_columns', None)  # 显示所有列
print(data[variables_to_plot])

# 绘制成对关系图，只包含指定的变量
g = sns.pairplot(data, vars=variables_to_plot, palette='coolwarm', height=2.5, hue='性别')
# 调整图形尺寸
g.fig.set_size_inches(15, 15)
for ax in g.axes.flatten():
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(left=False, bottom=False)  # 移除刻度线
plt.show()





















