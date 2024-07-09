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

# 查看数据基本信息
print(data.info())

# 确保系统中有中文字体，并设置为 SimHei
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决坐标轴负号显示问题


# 数据清洗

# 替换column的信息
data['性别'] = data['性别'].replace({'男': 'M', '女': 'W'})
# 检查 '性别' 列的数据类型和值
print(data['性别'].dtype)
print(data['性别'].unique())
# 确保 '性别' 列中没有缺失值
data = data.dropna(subset=['性别'])

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


# 计算相关系数

# 指定要计算相关系数的列
columns_to_analyze = ['近一年AR分数平均月变化', '近三个月AR分数平均月变化', '发病前体重', '当前体重（kg）', '身高（厘米）', '体重差值（kg）']

# 分别根据性别计算相关系数矩阵
male_data= data[data['性别'] == 'M'][columns_to_analyze]
female_data = data[data['性别'] == 'W'][columns_to_analyze]
male_correlation_matrix = male_data.corr()
female_correlation_matrix = female_data.corr()


# 绘制男性的相关系数矩阵热力图
plt.figure(figsize=(15, 15))
sns.heatmap(male_correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('男性的相关系数矩阵')
plt.show()

# 绘制女性的相关系数矩阵热力图
plt.figure(figsize=(15, 15))
sns.heatmap(female_correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('女性的相关系数矩阵')
plt.show()


# 回归分析

columns_to_regression = ['发病前体重', '当前体重（kg）', '身高（厘米）']
# 自变量
X = data[columns_to_regression]

# 添加常数项
X = sm.add_constant(X)

# 因变量
y_month = data['近三个月AR分数平均月变化']
y_all = data['近一年AR分数平均月变化']

# 进行回归分析
model_month = sm.OLS(y_month, X).fit()
model_all = sm.OLS(y_all, X).fit()

# 输出回归分析结果
print(model_month.summary())
print(model_all.summary())