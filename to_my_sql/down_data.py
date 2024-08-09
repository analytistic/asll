import shutil
import yaml
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.edge.options import Options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import logging



# 设置日志
logging.basicConfig(
    filename='web_scraping.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)


def init(config_file):
    """
    初始化，配置driver，读取config

    :param config_file:
    :return: config,edge_options
    """

    # 读取 YAML 配置文件
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)

    #  创建数据文件夹
    file_path = os.path.join(os.getcwd(), config["download_directory"])
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    # 配置下载目录
    prefs = {
        "download.default_directory": file_path
    }


    # 创建 Options 实例
    edge_options = Options()
    edge_options.add_experimental_option("prefs", prefs)


    # 清空data
    if os.path.exists(file_path) and os.path.isdir(file_path):
        for filename in os.listdir(file_path):
            file_path = os.path.join(os.getcwd(),config["download_directory"],filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    logging.info(f'删除{file_path}成功')
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    logging.info(f'删除{file_path}成功')

            except Exception as e:
                logging.error(f'删除{file_path}失败')


    return config, edge_options


            # 数据导出函数
def data_imp(config):
    """
    导出数据
    :return:
    """

    # 创建实例
    service = Service(executable_path=config["web_driver_path"])
    driver = webdriver.Chrome(service=service)
    driver.get(config["web"])


    # 切换class
    re = driver.find_element(By.XPATH, "//div[@class='login-form__operation']/span[text()='用户名密码登录']")
    re.click()


    # 输入账号
    wait = WebDriverWait(driver, 10)
    input_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".login-form__control input.control.ant-input")))
    password_input_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".login-form__control input[type='password']")))


    # 输入密码
    input_element.send_keys(config["web_user"])
    password_input_element.send_keys(config["web_password"])


    # 点击按钮
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".login-form__sumb button.control-button")))
    login_button.click()

    time.sleep(5)
    # 数据导出
    menu_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[span[text()='数据导出']]")))
    menu_item.click()


    try:
        # 等待直到加载动画或遮罩层消失
        wait = WebDriverWait(driver, 20)
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.loading.ant-spin.ant-spin-spinning")))

        # 等待“敏感信息不脱敏”按钮可点击
        sensitive_info_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '敏感信息不脱敏')]"))
        )
        driver.execute_script("arguments[0].click();", sensitive_info_button)

        # 等待全选元素可点击
        select_all_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '全选')]")))
        driver.execute_script("arguments[0].click();", select_all_button)

        # 等待导出元素点击
        export_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='导 出']]")))
        export_button.click()

        confirm_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'ant-btn-primary') and .//span[text()='确 定']]"))
        )
        driver.execute_script("arguments[0].click();", confirm_button)

        more_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='更多']"))
        )
        driver.execute_script("arguments[0].click();", more_button)

    finally:
        # 关闭浏览器
        time.sleep(5)  # 等待页面加载
        driver.quit()




def data_down(config, edge_options):
    """
    下载数据
    :param config:
    :param edge_options:
    :return:
    """

    # 创建WebDriver
    service = Service(executable_path=config["web_driver_path"])
    driver = webdriver.Chrome(service = service, options=edge_options)
    driver.get(config["web"])


    # 切换class
    re = driver.find_element(By.XPATH, "//div[@class='login-form__operation']/span[text()='用户名密码登录']")
    re.click()


    # 输入账号
    wait = WebDriverWait(driver, 10)
    input_element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".login-form__control input.control.ant-input")))
    password_input_element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".login-form__control input[type='password']")))


    # 输入密码
    input_element.send_keys(config["web_user"])
    password_input_element.send_keys(config["web_password"])


    # 点击按钮
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".login-form__sumb button.control-button")))
    login_button.click()


    # 数据导出
    menu_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[span[text()='数据导出']]")))
    menu_item.click()


    try:
        wait = WebDriverWait(driver, 20)
        more_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='更多']"))
        )
        driver.execute_script("arguments[0].click();", more_button)

        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.loading.ant-spin.ant-spin-spinning")))

        # 定位第一个“数据导出”元素并点击
        first_export_button = driver.find_element(By.XPATH,
                                                  "//ul[@class='export-history-list']/li[1]//span[@class='export-file-name cursor']")
        driver.execute_script("arguments[0].click();", first_export_button)

        # 记录成功信息
        logging.info('成功下载数据')

    except Exception as e:
        # 记录失败信息和异常信息
        logging.error('操作失败: %s', e)


    finally:
        time.sleep(60)  # 等待下载
        # 关闭浏览器
        driver.quit()



if __name__ == "__main__":
    config_file = 'config.yaml'
    edge_options=[]
    config={}

    config, edge_options =init(config_file)

    data_imp(config)
    # time.sleep(600)
    # data_down()



