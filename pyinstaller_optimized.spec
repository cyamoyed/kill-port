# 优化的PyInstaller配置文件
# 用于减小打包体积和提高启动速度
# Windows/Linux: --onedir 模式 (无临时解压, 启动快)
# macOS: --onedir + BUNDLE (.app)

import os
import sys

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[os.path.abspath('.')],
    binaries=[],
    datas=[],
    hiddenimports=['PyQt5.QtCore', 'PyQt5.QtWidgets', 'PyQt5.QtGui'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'numpy',
        'scipy',
        'matplotlib',
        'pandas',
        'PIL',
        'IPython',
        'jupyter',
        'test',
        'unittest',
        'email',
        'http',
        'xml',
        'html',
        'urllib',
        'ftplib',
        'bz2',
        'sqlite3',
        'concurrent',
        'multiprocessing',
        'asyncio',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='kill-port',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# macOS: bundle into .app
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='kill-port.app',
        icon=None,
        bundle_identifier=None,
    )
