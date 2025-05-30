import os
import sys
import threading
from flask import Flask, render_template, request, send_file
import tabula
import pandas as pd
import pystray
from PIL import Image
import tempfile
import webbrowser
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def create_tray_icon():
    try:
        # 创建系统托盘图标
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.png')
        if not os.path.exists(icon_path):
            # 如果图标不存在，创建一个简单的图标
            img = Image.new('RGB', (64, 64), color='red')
            img.save(icon_path)
        
        icon = pystray.Icon(
            "pdf_extractor",
            Image.open(icon_path),
            "PDF表格提取器",
            menu=pystray.Menu(
                pystray.MenuItem(
                    "退出",
                    lambda: icon.stop()
                )
            )
        )
        return icon
    except Exception as e:
        logger.error(f"创建系统托盘图标时出错: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return '没有选择文件', 400
        
        file = request.files['file']
        if file.filename == '':
            return '没有选择文件', 400
        
        if not file.filename.lower().endswith('.pdf'):
            return '请上传PDF文件', 400
        
        # 保存上传的文件
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(pdf_path)
        
        # 使用tabula-py提取表格
        tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
        
        if not tables:
            return '未找到表格', 400
        
        # 创建Excel文件
        excel_filename = os.path.splitext(file.filename)[0] + '.xlsx'
        excel_path = os.path.join(app.config['UPLOAD_FOLDER'], excel_filename)
        
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            for i, table in enumerate(tables):
                table.to_excel(writer, sheet_name=f'Table_{i+1}', index=False)
        
        # 返回Excel文件
        return send_file(
            excel_path,
            as_attachment=True,
            download_name=excel_filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    except Exception as e:
        logger.error(f"处理文件时出错: {e}")
        return str(e), 500

def run_flask():
    if getattr(sys, 'frozen', False):
        template_folder = os.path.join(sys._MEIPASS, 'templates')
        app.template_folder = template_folder
    
    app.run(port=5000, debug=False)

def open_browser():
    webbrowser.open('http://127.0.0.1:5000')

def main():
    try:
        # 启动Flask服务器
        server_thread = threading.Thread(target=run_flask, daemon=True)
        server_thread.start()
        
        # 打开浏览器
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        # 创建系统托盘图标
        icon = create_tray_icon()
        if icon:
            icon.run()
        else:
            logger.error("无法创建系统托盘图标")
            sys.exit(1)
    
    except Exception as e:
        logger.error(f"程序启动时出错: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 