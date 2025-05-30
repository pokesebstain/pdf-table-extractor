#!/bin/bash

# 确保Docker已安装
if ! command -v docker &> /dev/null; then
    echo "错误: 请先安装Docker"
    exit 1
fi

# 构建Docker镜像
echo "开始构建Docker镜像..."
docker build -t pdf-extractor-windows .

# 运行容器并复制生成的文件
echo "开始打包Windows应用..."
docker run --name pdf-extractor-build pdf-extractor-windows
docker cp pdf-extractor-build:/app/dist/PDF表格提取器 ./dist/PDF表格提取器-Windows
docker rm pdf-extractor-build

echo "打包完成！Windows版本的应用程序已保存在 ./dist/PDF表格提取器-Windows 目录中" 