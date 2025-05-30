# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# 确保目录存在
if not os.path.exists('templates'):
    os.makedirs('templates')
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# 收集所有需要的数据文件
datas = [
    ('templates', 'templates'),
    ('uploads', 'uploads'),
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
    'pkg_resources.markers',
    'pkg_resources.extern',
    'pkg_resources._vendor',
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
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
    name='PDF表格提取器',
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
    icon=None,
    version='1.0.0',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PDF表格提取器',
) 