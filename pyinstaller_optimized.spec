# 优化的PyInstaller配置文件
# 用于减小打包体积和提高启动速度

import os
import sys

block_cipher = None

# 基础配置
a = Analysis(
    ['main.py'],
    pathex=[os.path.abspath('.')],
    binaries=[],
    datas=[],
    hiddenimports=['PyQt5.QtCore', 'PyQt5.QtWidgets', 'PyQt5.QtGui'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        'tkinter',  # 排除tkinter，因为我们使用PyQt5
        'numpy',    # 排除不需要的库
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
        'gzip',
        'bz2',
        'zipfile',
        'tarfile',
        'sqlite3',
        'decimal',
        'fractions',
        'statistics',
        'concurrent',
        'multiprocessing',
        'threading',
        'queue',
        'socket',
        'select',
        'selectors',
        'asyncio',
        'contextlib',
        'functools',
        'itertools',
        'collections',
        'abc',
        'bisect',
        'heapq',
        'array',
        'ctypes',
        'inspect',
        'traceback',
        'logging',
        'warnings',
        'weakref',
        'gc',
        'atexit',
        'signal',
        'time',
        'datetime',
        'calendar',
        'locale',
        'string',
        're',
        'difflib',
        'textwrap',
        'unicodedata',
        'trace',
        'pickle',
        'copy',
        'pprint',
        'reprlib',
        'enum',
        'types',
        'typing',
        'dataclasses',
        'contextvars',
        'zoneinfo',
        'asyncio',
        'concurrent',
        'multiprocessing',
        'threading',
        'queue',
        'socket',
        'select',
        'selectors',
        'http',
        'urllib',
        'ftplib',
        'gzip',
        'bz2',
        'zipfile',
        'tarfile',
        'sqlite3',
        'decimal',
        'fractions',
        'statistics',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Windows 配置
if sys.platform == 'win32':
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
        strip=True,  # 启用符号表剥离
        upx=True,    # 启用UPX压缩
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,  # GUI模式
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None
    )
# macOS 配置
elif sys.platform == 'darwin':
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
        strip=True,  # 启用符号表剥离
        upx=True,    # 启用UPX压缩
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,  # GUI模式
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None
    )
    app = BUNDLE(
        exe,
        name='kill-port.app',
        icon=None,
        bundle_identifier=None
    )
# Linux 配置
else:
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
        strip=True,  # 启用符号表剥离
        upx=True,    # 启用UPX压缩
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,  # GUI模式
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None
    )