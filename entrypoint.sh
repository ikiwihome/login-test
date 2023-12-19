#!/bin/sh

cd /app     # 进入/app目录
python -V  # 查看Python版本
pip -V     # 查看pip版本
pip list --format=freeze > data/requirements.txt  # 列出所有安装的Python包并保存到requirements.txt文件中
cat data/requirements.txt  # 显示requirements.txt文件内容
python app.py  # 运行app.py脚本
