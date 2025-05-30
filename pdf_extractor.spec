# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# 确保目录存在
for dir_name in ['templates', 'uploads', 'assets']:
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

# 创建默认图标
from PIL import Image
icon_path = os.path.join('assets', 'icon.png')
if not os.path.exists(icon_path):
    img = Image.new('RGB', (64, 64), color='red')
    img.save(icon_path)

# 收集所有需要的数据文件
datas = [
    ('templates', 'templates'),
    ('assets', 'assets'),
]

# 收集所有需要的隐藏导入
hiddenimports = [
    'tabula',
    'tabula.io',
    'pandas',
    'openpyxl',
    'PIL',
    'pystray',
    'PIL._tkinter_finder',
    'pkg_resources.py2_warn',
    'jpype',
    'flask',
    'werkzeug',
    'jinja2',
]

# 添加 Java 相关文件
java_home = os.environ.get('JAVA_HOME')
if java_home:
    java_bin = os.path.join(java_home, 'bin')
    if sys.platform == 'win32':
        binaries = [(os.path.join(java_bin, 'server', 'jvm.dll'), 'java/bin/server')]
    elif sys.platform == 'darwin':
        binaries = [(os.path.join(java_bin, 'libjli.dylib'), 'java/bin')]
    else:
        binaries = [(os.path.join(java_bin, 'libjvm.so'), 'java/bin')]
else:
    binaries = []

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PDFTableExtractor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
    version='file_version_info.txt',
)

# 创建版本信息文件
version_info = '''
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u''),
         StringStruct(u'FileDescription', u'PDF Table Extractor'),
         StringStruct(u'FileVersion', u'1.0.0'),
         StringStruct(u'InternalName', u'PDFTableExtractor'),
         StringStruct(u'LegalCopyright', u''),
         StringStruct(u'OriginalFilename', u'PDFTableExtractor.exe'),
         StringStruct(u'ProductName', u'PDF Table Extractor'),
         StringStruct(u'ProductVersion', u'1.0.0')])
    ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''

with open('file_version_info.txt', 'w') as f:
    f.write(version_info)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PDFTableExtractor',
) 