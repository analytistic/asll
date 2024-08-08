import time
from selenium import webdriver
import os
import json

driver = webdriver.Edge()

try:
    # 打开als主页并手动登录
    driver.get("https://als.ashermed.com/web/login")
    time.sleep(120)  # 给用户足够的时间手动登录

    # 获取登录后的 cookie
    cookies = driver.get_cookies()

    # 打印当前工作目录
    print("Current working directory: ", os.getcwd())

    # 将 cookie 保存到文件
    with open("cookies.json", "w") as file:
        json.dump(cookies, file)
    print("Cookies saved successfully.")
finally:
    driver.quit()


