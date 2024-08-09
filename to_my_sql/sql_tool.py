import yaml
import pandas as pd
import mysql.connector
from mysql.connector import Error
import os
import logging
import numpy as np
import re
from tqdm import tqdm
import sys
sys.setrecursionlimit(3000)  # 将递归深度限制设置为3000



# 设置日志
logging.basicConfig(
    filename='import_data.log',  # 日志文件名
    level=logging.INFO,          # 日志级别
    format='%(asctime)s - %(levelname)s - %(message)s',  # 日志格式
    encoding='utf-8'
)



# 加载设置文件
def load_mysql_config(config_file):
    try:
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logging.error(f"Error loading MySQL config file: {e}")
        raise



def create_connection(config):
    """
    创建数据库连接
    :param config:
    :return:
    """

    try:
        connection = mysql.connector.connect(
            host=config["host"],
            user=config["user"],
            password=config["password"],
            database=config["database"],
            charset=config['charset']
        )
        logging.info("Database connection created successfully.")
        return connection

    except Error as e:
        logging.error(f"Error creating database connection: {e}")
        return None



def sanitize_column_name(col_name):
    # 修改非法列名
    col_name = col_name.strip()
    if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', col_name):
        return col_name
    else:
        return f'_{col_name}'



def generate_create_basic_info_table_query(df, sheet_name, primary_key='患者编号'):
    column_type = 'TEXT'  # Or use 'VARCHAR(255)' depending on the data
    columns = ', '.join([f'`{sanitize_column_name(col)}` {column_type}' for col in df.columns])

    return f"""
        CREATE TABLE IF NOT EXISTS `{sheet_name}` (
            `{primary_key}` VARCHAR(255) PRIMARY KEY,
            {columns}
        );
    """



def generate_create_other_table_query(df, sheet_name, foreign_key='患者编号'):
    column_type = 'TEXT'  # Or use 'VARCHAR(255)' depending on the data
    columns = ', '.join([f'`{sanitize_column_name(col)}` {column_type}' for col in df.columns if col != foreign_key])

    return f"""
        CREATE TABLE IF NOT EXISTS `{sheet_name}` (
            id INT AUTO_INCREMENT PRIMARY KEY,
            {columns},
            `{foreign_key}` VARCHAR(255),
            FOREIGN KEY (`{foreign_key}`) REFERENCES 基本信息(`患者编号`)
        );
    """



def create_table(cursor, sheet_name, df):
    """
    创建表
    :param cursor:
    :param sheet_name:
    :param df:
    :return:
    """

    if sheet_name == '基本信息':
        create_table_query = generate_create_basic_info_table_query(df, sheet_name, primary_key='患者编号')

    else:
        create_table_query = generate_create_other_table_query(df, sheet_name, foreign_key='患者编号')


    drop_table_query = f"DROP TABLE IF EXISTS `{sheet_name}`;"


    try:
        cursor.execute(drop_table_query)
        logging.info(f"Attempting to drop table `{sheet_name}`.")

    except Error as e:
        logging.error(f"Error dropping table `{sheet_name}`: {e}")


    try:
        cursor.execute(create_table_query)
        logging.info(f"Table `{sheet_name}` created successfully.")

    except Error as e:
        logging.error(f"Error creating table `{sheet_name}`: {e}")




def import_data(cursor, sheet_name, df):
    """
    导入数据
    :param cursor:
    :param sheet_name:
    :param df:
    :return:
    """

    df = df.replace(np.nan, None)
    columns = [f'`{sanitize_column_name(col)}`' for col in df.columns]


    for i, row in df.iterrows():
        placeholders = ', '.join(['%s'] * len(row))
        insert_query = f"""
            INSERT IGNORE INTO `{sheet_name}` ({', '.join(columns)}) 
            VALUES ({placeholders});
        """

        try:
            cursor.execute(insert_query, tuple(row))
            logging.info(f"Successfully inserted row {i} into `{sheet_name}`.")

        except Error as e:
            logging.error(f"Error inserting row {i} into `{sheet_name}`: {e}, row {i}")



def import_excel_to_mysql(excel_folder, config_file):
    """
    pd读取 Excel 文件，导入数据库
    :param excel_folder:
    :param config_file:
    :return:
    """

    config = load_mysql_config(config_file)
    connection = create_connection(config)


    if connection is None:
        return

    cursor = connection.cursor()

    try:
        # 遍历所有 Excel 文件
        for file_name in os.listdir(excel_folder):
            if file_name.endswith('.xlsx'):
                file_path = os.path.join(excel_folder, file_name)
                xls = pd.ExcelFile(file_path)
                sheet_names = xls.sheet_names

                for sheet_name in tqdm(sheet_names, desc=f"Processing {file_name}", unit='sheet'):
                    df = pd.read_excel(file_path, sheet_name=sheet_name)

                    if sheet_name in {'其他辅助检查', '治疗经历'}:
                        continue

                    create_table(cursor, sheet_name, df)
                    import_data(cursor, sheet_name, df)
                    connection.commit()
                    logging.info(f"Data from `{sheet_name}` imported successfully.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        cursor.close()
        connection.close()




if __name__ == "__main__":
    # 设置路径
    excel_folder = os.path.join(os.getcwd(), 'data_to_mysql')  # 数据文件夹路径
    config_file = os.path.join(os.getcwd(), 'config.yaml')  # 配置文件路径

    # 更新数据库
    import_excel_to_mysql(excel_folder, config_file)
