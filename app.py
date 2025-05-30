import os
from flask import Flask, request, render_template, send_file
import tabula
import pandas as pd
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB max file size

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_pdf_tables(filepath, source_filename):
    """处理单个PDF文件中的所有表格"""
    try:
        # 使用tabula-py提取表格
        tables = tabula.read_pdf(filepath, pages='all')
        processed_tables = []
        
        for index, table in enumerate(tables, 1):
            if not table.empty:
                # 转置表格
                table_t = table.transpose()
                # 将原来的列名作为新的索引
                table_t.columns = table_t.iloc[0]
                # 删除第一行（原来的列名）
                table_t = table_t.iloc[1:]
                # 重置索引
                table_t = table_t.reset_index()
                # 重命名第一列
                table_t = table_t.rename(columns={'index': 'Row_Labels'})
                
                # 添加元数据列
                table_t.insert(0, 'Source_File', source_filename)
                table_t.insert(1, 'Table_Number', f'Table_{index}')
                table_t.insert(2, 'Page_Number', f'Page_{index}')
                
                processed_tables.append(table_t)
        
        return processed_tables
    except Exception as e:
        print(f"Error processing {source_filename}: {str(e)}")
        return []

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return 'No files uploaded', 400
    
    files = request.files.getlist('files[]')
    if not files or files[0].filename == '':
        return 'No selected files', 400

    # 检查所有文件是否都是PDF
    if not all(allowed_file(f.filename) for f in files):
        return 'Only PDF files are allowed', 400

    all_tables = []
    processed_files = []
    errors = []
    
    try:
        for file in files:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            try:
                file.save(filepath)
                tables = process_pdf_tables(filepath, filename)
                
                if tables:
                    all_tables.extend(tables)
                    processed_files.append(filename)
                else:
                    errors.append(f"No tables found in {filename}")
                
            except Exception as e:
                errors.append(f"Error processing {filename}: {str(e)}")
            finally:
                # 清理临时文件
                if os.path.exists(filepath):
                    os.remove(filepath)
        
        if not all_tables:
            error_msg = "No tables found in any of the uploaded PDFs"
            if errors:
                error_msg += f"\nErrors: {'; '.join(errors)}"
            return error_msg, 400
        
        # 合并所有表格
        combined_df = pd.concat(all_tables, ignore_index=True)
        
        # 生成带时间戳的输出文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f'combined_tables_{timestamp}.xlsx'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # 创建Excel写入器
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # 写入合并后的表格
            combined_df.to_excel(writer, sheet_name='All Tables', index=False)
            
            # 为每个源文件创建单独的工作表
            for source_file in processed_files:
                source_tables = combined_df[combined_df['Source_File'] == source_file]
                if not source_tables.empty:
                    sheet_name = os.path.splitext(source_file)[0][:31]  # Excel工作表名称限制为31字符
                    source_tables.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # 返回生成的Excel文件
        return send_file(
            output_path,
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) 