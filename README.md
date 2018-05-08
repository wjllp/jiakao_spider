# jiakao_spider
爬取驾考网考试信息

# 使用环境
Python 3.*

# 使用方法
- 下载本项目到电脑
- 运行```pip3 install -r requirements.txt```安装所需环境
- 创建MySQL数据库
- 运行```jiakao.sql```创建表
- 运行```python3 regist.py```注册用户，输入邮箱、考场名称、考试科目即可
- 使用crontab设置定时任务即可，建议设置每20分钟执行一次
- 当有新指标出来时用户便会收到邮件

# 适用地区
- 目前只支持湖北省鄂州市区域使用，更多功能等待开发中
