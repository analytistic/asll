import time
from sql_tool import import_excel_to_mysql
from down_data import init,data_imp,data_down
import os
import sys
sys.setrecursionlimit(2000)  # 将递归深度限制设置为2000


if __name__ == "__main__":

    # 设置路径
    excel_folder = os.path.join(os.getcwd(),'data_to_mysql')  # 数据文件夹路径
    config_file = os.path.join(os.getcwd(),'config.yaml')  # 配置文件路径


    # 抓取数据
    config = {}
    edge_options = []
    config, edge_options = init(config_file)
    data_imp(config)
    time.sleep(600)
    data_down(config,edge_options)


    # 更新数据库
    import_excel_to_mysql(excel_folder, config_file)



