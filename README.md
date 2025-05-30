# PDF表格提取器

一个用于从PDF文件中提取表格并转换为Excel文件的桌面应用程序。

## 功能特点

- 支持多个PDF文件批量处理
- 自动提取PDF中的所有表格
- 转换表格为Excel格式
- 支持表格转置功能
- 保留源文件、表格编号等元数据
- 简洁现代的用户界面
- 系统托盘运行，方便访问

## 系统要求

- Windows 7/10/11
- Java Runtime Environment (JRE) 8 或更高版本

## 使用说明

1. 双击运行应用程序
2. 在系统托盘中找到应用图标
3. 点击"打开"启动Web界面
4. 拖拽或选择PDF文件上传
5. 等待处理完成后自动下载Excel文件

## 注意事项

- 首次运行可能需要允许防火墙访问
- 确保已安装Java运行环境
- 上传文件大小限制为32MB
- 处理大文件时可能需要等待较长时间

## 开发环境设置

```bash
# 克隆仓库
git clone [repository-url]

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 运行应用
python main.py
```

## 技术栈

- Flask - Web框架
- tabula-py - PDF表格提取
- pandas - 数据处理
- Bootstrap - 前端界面