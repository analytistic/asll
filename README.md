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
    ```angular2html
    cd <you_path>/to_my_sql
   ```
2. 虚拟环境激活文件路径
    ```angular2html
    call <you_venv_path>\venv\Scripts\activate.bat
   
### run_main.sh

`run.sh`文件是mac用户使用的，也同bat文件一样调整路径即可:
1. 设置工作目录
```angular2html
cd /<path_to>/asl/to_my_sql || exit
```

2. 虚拟环境激活文件路径
```angular2html
source /<path_to>/venv/bin/activate
```


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
   ```angular2html
   D: <you_path>\to_my_sql\run_main.bat
   ```
## 四. mac用户可以使用launchd定时运行任务

在 macOS 上，你可以使用 `launchd` 配置文件来定时运行任务。以下是具体步骤：

### 1. 创建或编辑 plist 文件

打开终端，并使用文本编辑器创建或编辑 plist 文件。以下示例使用 `nano` 编辑用户范围的 plist 文件：
      
```angular2html
nano ~/Library/LaunchAgents/com.example.<up_date_sql>.plist
```

### 2. 配置XML
比如设置任务每天凌晨 1:30 运行，复制即可
```angular2html
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- 任务标签 -->
    <key>Label</key>
    <string>com.example.up_date_sql</string>
    
    <!-- 运行的程序的路径 -->
    <key>ProgramArguments</key>
    <array>
        <string>/Users/<your_path_to>/run_main.sh</string>
    </array>
    
    <!-- 设置每天凌晨 1:30 运行 ，时间在这里改就行-->
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>1</integer>
        <key>Minute</key>
        <integer>30</integer>
    </dict>
    
    <!-- 确保在任务首次加载时立即运行，可以删掉 -->
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>

```
### 3. 保存并退出
在 `nano` 中，按 `Ctrl+O` 保存文件，然后按 `Enter` 确认。按 `Ctrl+X` 退出编辑器

### 4. 设置文件权限

确保 plist 文件有正确的权限：


```angular2html
chmod 644 ~/Library/LaunchAgents/com.example.<up_date_sql>.plist
```

### 4. 启动并加载任务
```angular2html
launchctl load ~/Library/LaunchAgents/com.example.<up_date_sql>.plist
```
# 阿里RDS数据库使用
## 1. 设置白名单
- 登录阿里云账号
- 在产品界面选择`云数据库RDS`
- 在左侧导航栏选择`实例列表`，地域选择`华东2上海`
- 点击`管理`，然后在左侧导航栏选择`白名单与安全组` ,然后选择`添加白名单分组`
- 然后添加自己的公网`ip地址`

## 2. 使用数据库
1. DMS网页端查询

可以使用DMS直接查看数据库。在实例列表登录数据库root账户即可。

2. 本地客户端查询

或者使用本地客户端，建议使用`MySQL workbench`，界面比较友好。
```angular2html
https://dev.mysql.com/downloads/workbench/
```
安装好后，添加连接:

- Connection Name: `rds_mysql巴拉巴拉`
- connection Method: `standard(TCP/IP)`
- Hostname: `rm-uf686mnkbma2165skpo.mysql.rds.aliyuncs.com`
- Port: `3306`
- Username: `root`
- Password: `XXXXXX`

然后连接即可



