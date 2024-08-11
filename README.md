# 数据库更新脚本（to_my_sql）

## 一. 安装
- Python 3.12
- pip
- chrome  <span style="color:red">（确保web_driver和chrome版本一致）</span>
- web_driver
    ```bash
    https://googlechromelabs.github.io/chrome-for-testing/

### 部署步骤

1. 克隆这个仓库
   ```bash
   git clone https://github.com/bonnieouyang/wentao_code.git
2. 安装环境
   ```bash
   pip install -r requirements.txt
3. 请确保用户对 "to_my_sql" 文件夹有足够权限

## 二. 文件说明

### config.yaml文件
1. 请在 "sql主机连接设置" 下配置
   1. 主机ip
   2. 用户名
   3. 密码
2. 请在 "数据库设置" 下设置需要更新的：  
   1. 数据库名称
   2. 主表名称（脚本默认主表主键和子表外键连接）
   3. 主键名称
   4. 外键名称
   5. 是否重建数据库
3. 请在 "爬虫脚本设置" 下设置：
   1. 文件下载路径（不需要改）
   2. 网页地址
   3. 用户
   4. 密码
   5. web_driver地址（这个得改）

### run_main.bat文件
1. 设置工作路径
    ```bash
    cd <you_path>/to_my_sql
   
2. 激活虚拟环境
    ```bash
    call <you_venv_path>\venv\Scripts\activate.bat

## 三. 使用 Windows 任务计划程序定时运行脚本

### 1. 打开任务计划程序
1. 按下 `Win + R` 组合键，打开“运行”对话框。
2. 输入 `taskschd.msc`，然后按回车键，打开任务计划程序。

### 2. 创建新的任务
1. 在任务计划程序窗口中，点击右侧的“**创建任务**”。
2. 在“创建任务”窗口中，填写以下内容：
   - **常规选项卡**：
     - **名称**：`sql数据库更新脚本巴拉巴拉`
     - **描述**：`巴拉巴拉`
     - **安全选项**：选择合适的用户或组，确保有足够权限更改`to_my_sql`文件夹的内容

### 3. 设置触发器

1. 转到“**触发器**”选项卡，点击“**新建**”。
2. 在“新建触发器”窗口中，选择触发器类型（如“每日”、“每周”等）。
3. 设置具体的时间和日期，例如每天上午 8:00。
4. 点击“**确定**”以保存触发器设置。

###  4. 配置操作

1. 转到“**操作**”选项卡，点击“**新建**”。
2. 在“新建操作”窗口中，选择“**启动程序**”作为操作类型。
3. 在“**程序/脚本**”字段中，输入批处理文件的完整路径，例如：
   ```bash
   D: <you_path>\to_my_sql\run_main.bat
