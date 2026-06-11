# 使用官方 Python 3.11 镜像，兼容性最好
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 先复制依赖清单，利用 Docker 缓存
COPY requirements.txt .

# 安装依赖，加上国内源，避免网络超时
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制所有项目代码
COPY . .

# 启动命令，必须用 $PORT，Railway 会自动替换
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]