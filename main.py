import os
import sys
import threading
from flask import Flask, render_template, request, send_file
import tabula
import pandas as pd
import pystray
from PIL import Image
import webbrowser
import logging
import tempfile
import atexit
import signal

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.join(os.path.dirname(__file__), 'uploads'))
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

def create_tray_icon():
    """创建系统托盘图标"""
    try:
        icon_path = resource_path(os.path.join('assets', 'icon.png'))
        if not os.path.exists(icon_path):
            # 如果图标不存在，创建一个简单的图标
            img = Image.new('RGB', (64, 64), color='red')
            img.save(icon_path)
        
        icon = pystray.Icon(
            "pdf_extractor",
            Image.open(icon_path),
            "PDF Table Extractor",
            menu=pystray.Menu(
                pystray.MenuItem(
                    "Exit",
                    lambda: stop_application()
                )
            )
        )
        return icon
    except Exception as e:
        logger.error(f"Error creating system tray icon: {e}")
        return None

def stop_application():
    """停止应用程序"""
    try:
        if hasattr(stop_application, 'icon') and stop_application.icon:
            stop_application.icon.stop()
        os._exit(0)
    except Exception as e:
        logger.error(f"Error stopping application: {e}")
        os._exit(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return 'No file selected', 400
        
        file = request.files['file']
        if file.filename == '':
            return 'No file selected', 400
        
        if not file.filename.lower().endswith('.pdf'):
            return 'Please upload a PDF file', 400
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            file.save(temp_pdf.name)
            pdf_path = temp_pdf.name
        
        # 使用tabula-py提取表格
        tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
        
        if not tables:
            os.unlink(pdf_path)
            return 'No tables found in the PDF', 400
        
        # 创建临时Excel文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_excel:
            excel_path = temp_excel.name
        
        # 写入Excel文件
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            for i, table in enumerate(tables):
                table.to_excel(writer, sheet_name=f'Table_{i+1}', index=False)
        
        # 清理临时PDF文件
        os.unlink(pdf_path)
        
        # 返回Excel文件
        return_data = send_file(
            excel_path,
            as_attachment=True,
            download_name=os.path.splitext(file.filename)[0] + '.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
        # 设置回调以清理临时Excel文件
        @atexit.register
        def cleanup():
            try:
                os.unlink(excel_path)
            except:
                pass
        
        return return_data
    
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        return str(e), 500

def run_flask():
    """运行Flask服务器"""
    if getattr(sys, 'frozen', False):
        # 如果是打包后的执行文件
        template_folder = resource_path('templates')
        app.template_folder = template_folder
    
    app.run(port=5000, debug=False)

def open_browser():
    """打开浏览器"""
    webbrowser.open('http://127.0.0.1:5000')

def main():
    try:
        # 启动Flask服务器
        server_thread = threading.Thread(target=run_flask, daemon=True)
        server_thread.start()
        
        # 等待服务器启动
        import time
        time.sleep(1)
        
        # 打开浏览器
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        # 创建系统托盘图标
        icon = create_tray_icon()
        if icon:
            stop_application.icon = icon
            icon.run()
        else:
            logger.error("Failed to create system tray icon")
            sys.exit(1)
    
    except Exception as e:
        logger.error(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    # 设置信号处理
    signal.signal(signal.SIGINT, lambda s, f: stop_application())
    signal.signal(signal.SIGTERM, lambda s, f: stop_application())
    
    main() 