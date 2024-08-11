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


# 读取 Mysql 置文件
def load_mysql_config(config_file):
    try:
        with open(config_file, 'r', encoding='utf_8_sig') as f:
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


# 修改非法列名
def sanitize_column_name(col_name):
    col_name = col_name.strip()
    if col_name and col_name[0].isdigit():
        col_name = '_' + col_name
    col_name = re.sub(r'[^\w\u4e00-\u9fff]', '_', col_name)

    return col_name

def create_table(cursor, sheet_name, df, config):

    basic_table_pk = config["basic_table_PK"]
    sub_table_fk = config["sub_table_fk"]

    # 创建主表列SQL
    def generate_create_basic_info_table_query(use_text=False, primary_key=basic_table_pk):
        column_type = 'TEXT' if use_text else 'VARCHAR(255)'
        columns = [sanitize_column_name(col) for col in df.columns]
        if primary_key in columns:
            columns.remove(primary_key)

        columns_reg = ', '.join([f'`{col}` {column_type}' for col in columns])

        return f"""
            CREATE TABLE IF NOT EXISTS `{sheet_name}` (
                `{primary_key}` VARCHAR(255) PRIMARY KEY,
                {columns_reg}
            );
        """


    # 创建子表列SQL
    def generate_create_sub_info_table_query(use_text=False, foreign_key=sub_table_fk):
        column_type = 'TEXT' if use_text else 'VARCHAR(255)'
        columns = [sanitize_column_name(col) for col in df.columns]
        if foreign_key in columns:
            columns.remove(foreign_key)
            columns_reg = ', '.join([f'`{col}` {column_type}' for col in columns])

            return f"""
                CREATE TABLE IF NOT EXISTS `{sheet_name}` (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    `{foreign_key}` VARCHAR(255),
                    {columns_reg},
                    FOREIGN KEY (`{foreign_key}`) REFERENCES {config["basic_table"]}(`{basic_table_pk}`)
                );
            """
        else:
            columns_reg = ', '.join([f'`{col}` {column_type}' for col in columns])

            return f"""
                CREATE TABLE IF NOT EXISTS `{sheet_name}` (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    {columns_reg}
                );
            """

    # try创建表
    def try_create_table(cursor, sheet_name, use_text=False):
        if sheet_name == config["basic_table"]:
            create_table_query = generate_create_basic_info_table_query(use_text)
        
        else:
            create_table_query = generate_create_sub_info_table_query(use_text)
            
        try:
            cursor.execute(create_table_query)
            logging.info(f"Table `{sheet_name}` created successfully with {'TEXT' if use_text else 'VARCHAR'}.")
            return True
        except Error as e:
            if 'Row size too large' in str(e):
                logging.warning(f"Row size too large error for table `{sheet_name}`. Trying TEXT columns.")
                return try_create_table(cursor, sheet_name, use_text=True)
            else:
                logging.error(f"Error creating table `{sheet_name}`: {e}")
                return False

    # # 删除表SQL
    # drop_table_query = f"DROP TABLE IF EXISTS `{sheet_name}`;"

    # # 删除旧表
    # try:
    #     cursor.execute(drop_table_query)
    #     logging.info(f"Attempting to drop table `{sheet_name}`.")
    #
    # except Error as e:
    #     logging.error(f"Error dropping table `{sheet_name}`: {e}")
    
    # 创建新表
    try_create_table(cursor, sheet_name, use_text=False)


# 获取sql表中col顺序
def get_column_order(cursor, table_name):
    cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")
    sql_columns = cursor.fetchall()
    column_order = [col[0] for col in sql_columns]
    return column_order


def import_data(cursor, sheet_name, df, config, connection):
    """
    插入数据，这里时间复杂度应该是O(row*col)
    :param cursor:
    :param sheet_name:
    :param df:
    :param config:
    :param connection:
    :return:
    """

    # 空值处理
    df = df.replace(np.nan, None)

    # 获取表的列顺序
    column_order = get_column_order(cursor, sheet_name)

    # 清理并匹配 DataFrame 列与表列
    df.columns = [sanitize_column_name(col) for col in df.columns]
    sanitized_columns = set(df.columns)  # 使用集合提高查找效率
    columns = [col for col in column_order if col in sanitized_columns]

    # 准备批量插入的数据
    rows = []
    for _, row in df.iterrows():
        rows.append(tuple(row[col] for col in columns))

    if rows:
        placeholders = ', '.join(['%s'] * len(columns))
        insert_query = f"""
            INSERT IGNORE INTO `{sheet_name}` ({', '.join(columns)}) 
            VALUES ({placeholders});
        """

        try:
            cursor.executemany(insert_query, rows)
            connection.commit()  # 提交当前事务
            logging.info(f"成功插入 {len(rows)} 行到 `{sheet_name}` 表中。")
        except Error as e:
            connection.rollback()  # 回滚当前事务
            logging.error(f"插入行到 `{sheet_name}` 表时发生错误: {e}")


# 检查数据库是否存在
def database_exists(cursor, database_name):
    try:
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        return database_name in databases
    except Error as e:
        logging.error(f"Error checking if database exists: {e}")
        raise


# 创建数据库
def create_database(cursor, database_name):
    try:
        cursor.execute(
            f"""
            CREATE SCHEMA `{database_name}` 
            DEFAULT CHARACTER SET utf8mb4 
            DEFAULT COLLATE utf8mb4_general_ci;
            """
        )
        logging.info(f"Database `{database_name}` created successfully.")
    except Error as e:
        logging.error(f"Error creating database `{database_name}`: {e}")
        raise


# 删除数据库
def delete_database(cursor, database_name):
    try:
        cursor.execute(f"DROP SCHEMA IF EXISTS `{database_name}`")
        logging.info(f"Database `{database_name}` deleted successfully.")
    except Error as e:
        logging.error(f"Error deleting database `{database_name}`: {e}")
        raise

def import_excel_to_mysql(excel_folder, config_file):
    """
    读取xlsx文件夹，导入数据库
    :param excel_folder:
    :param config_file:
    :return:
    """

    config = load_mysql_config(config_file)
    connection = create_connection(config)

    if connection is None:
        return

    cursor = connection.cursor()

    # 选择是否rebuild
    database_name = config["database"]
    if database_exists(cursor, database_name):
        if config["recreate"] == "YES":
            logging.info(f"recreate option is enabled. Proceeding with deleting and recreating the database `{database_name}`.")
            delete_database(cursor, database_name)
            create_database(cursor, database_name)
        else:
            logging.info(f"Database `{database_name}` exists and rebuild is not required. Skipping deletion.")
    else:
        logging.info(f"Database `{database_name}` does not exist. Proceeding with creation.")
        create_database(cursor,database_name)

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

                    create_table(cursor, sheet_name, df, config)
                    import_data(cursor, sheet_name, df, config, connection)
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
