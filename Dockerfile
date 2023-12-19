FROM python:3.9-alpine3.18

# alpine源替换为腾讯源，更新软件
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.cloud.tencent.com/g' /etc/apk/repositories
RUN apk update
RUN apk add --update --no-cache \
       bash \
       nano \
       curl \
       wget \
       tzdata \
    && rm -rf /var/cache/apk/* /tmp/*

# pip源更换为腾讯云镜像
RUN pip install -i https://mirrors.cloud.tencent.com/pypi/simple/ -U pip
RUN pip config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple/
RUN pip config set install.mirrors https://mirrors.cloud.tencent.com/pypi/simple/
RUN pip config set install.use-mirrors true
RUN pip config set install.trusted-host mirrors.cloud.tencent.com

WORKDIR /app

# 设置为中文，时区为北京时间，alpinelinux更换为腾讯云镜像
ENV LANG=zh_CN.UTF-8 \
    TZ=Asia/Shanghai

COPY . .

# 安装flask、requests、aiohttp、asyncio、flask_jwt_extended等Python库
RUN pip install flask requests aiohttp asyncio flask_jwt_extended

# 删除pip缓存
RUN rm -rf pip && pip cache purge

# 公开65432端口
EXPOSE 65432

# 复制entrypoint.sh脚本到容器中的entrypoint.sh路径
COPY entrypoint.sh /entrypoint.sh

# 为entrypoint.sh脚本添加可执行权限
RUN ["chmod", "+x", "/entrypoint.sh"]

# 设置容器启动时的入口点为entrypoint.sh脚本
ENTRYPOINT ["/entrypoint.sh"]
