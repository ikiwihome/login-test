# -*- coding: utf-8 -*-
import os, hashlib, jwt
from flask import Flask, request, make_response, render_template, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

# 随机的高强度密钥
app.secret_key = 'vN8Tq6grBKAl9ZOh6i71Or6'
password_file = './data/password'
default_pw = 'admin'

# token 90天后过期
max_age = 90 * 24 * 60 * 60  # 90天 * 24小时 * 60分钟 * 60秒

@app.route('/')
def index():
    token = request.cookies.get('token')
    if validate_token(token):
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # 如果文件不存在则创建默认密码文件
    if not os.path.exists(password_file):
        os.makedirs(os.path.dirname(password_file), exist_ok=True)
        with open(password_file, 'w') as f:
            f.write(default_pw)

    # 读取密码文件
    with open(password_file) as f:
        default_password = f.read().strip()

    # 生成密码的哈希值
    hashed_stored = hashlib.sha256(default_password.encode("utf-8")).hexdigest()

    if request.method == 'POST':
        # 从表单中获取密码
        hashed_password = request.form['hash']
        # 验证密码的正确性
        if hashed_password == hashed_stored:
            # 如果密码验证通过
            token = generate_token()
            # 生成一个令牌
            resp = make_response(redirect(url_for('index')))
            # 创建一个重定向响应对象，跳转到相册页面
            resp.set_cookie('token', token, max_age=max_age)
            # 设置cookie，保存令牌，设置过期时间为max_age
            return resp
            # 返回响应对象
        else:
            # 如果密码验证不通过
            return render_template('login.html', error='密码输入错误！')
            # 返回登录页面模板，并传递错误信息
    return render_template('login.html')
    # 返回登录页面模板


@app.route('/logout')
def logout():
    # 生成一个响应对象并重定向到登录页面
    resp = make_response(redirect(url_for('login')))
    # 设置一个名为'token'的cookie，过期时间为0
    resp.set_cookie('token', '', expires=0)
    # 返回响应对象
    return resp


def generate_token():
    # 获取当前时间加上90天
    expiration = datetime.utcnow() + timedelta(days=90)

    # 定义一个字典，包含一个键值对，键为'exp'，值为expiration
    data = {
        'exp': expiration
    }

    # 使用jwt.encode()函数将data字典进行编码，使用app.secret_key作为密钥，algorithm参数指定加密算法为'HS256'
    token = jwt.encode(data, app.secret_key, algorithm='HS256')

    # 返回编码后的token
    return token


def validate_token(token):
    try:
        # 尝试解码token
        data = jwt.decode(token, app.secret_key, algorithms=['HS256'])
        # 获取token的过期时间
        expired_date = data.get('exp')
        # 如果过期时间不存在，则返回False
        if expired_date is None:
            return False
        # 将过期时间转换为时间戳
        print_date = datetime.fromtimestamp(expired_date)
        # 将过期时间格式化为指定格式的字符串
        print(print_date.strftime('%Y-%m-%d %H:%M:%S'))
        # 返回True表示token有效
        return True
    # 如果token已过期，执行以下代码
    except jwt.ExpiredSignatureError:
        # 返回False表示token无效
        return False
    # 如果token无效，执行以下代码
    except jwt.InvalidTokenError:
        # 返回False表示token无效
        return False


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=65432, debug=True)
