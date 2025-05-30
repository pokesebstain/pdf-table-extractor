import os
import sys
import webbrowser
import threading
from PIL import Image
import pystray
from pystray import MenuItem as item
from app import app

def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def create_icon():
    """创建系统托盘图标"""
    # 创建一个简单的图标（这里创建一个纯色图标，您可以替换为自己的图标文件）
    width = 64
    height = 64
    color = 'blue'
    image = Image.new('RGB', (width, height), color)
    return image

def open_browser():
    """打开默认浏览器访问应用"""
    webbrowser.open('http://localhost:8080')

def on_quit():
    """退出应用"""
    icon.stop()
    os._exit(0)

def run_flask():
    """运行Flask应用"""
    app.run(host='localhost', port=8080)

def main():
    # 创建并启动Flask线程
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # 创建系统托盘图标
    global icon
    icon = pystray.Icon(
        "pdf_extractor",
        create_icon(),
        "PDF表格提取器",
        menu=pystray.Menu(
            item('打开', open_browser),
            item('退出', on_quit)
        )
    )

    # 显示系统托盘图标并等待
    icon.run()

if __name__ == '__main__':
    main() 