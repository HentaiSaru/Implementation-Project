# -*- mode: python ; coding: utf-8 -*-

# 這邊可設置Key(安慰用)
# 不設置就是把 = 後面刪除
block_cipher = pyi_crypto.PyiBlockCipher(key='key')


a = Analysis(
    ['display.py'], # 設置要打包的 .py 文件
    pathex=[],
    binaries=[],
    datas=[('display.ico', '.')], # 程式所需的依賴檔案 (例如Icon)
    hiddenimports=[], # 排除不需要的模塊
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='display', # 打包後的 exe 文件名
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True, # 啟用 upx 壓縮 (需要再 Scripts , 放入 upx.exe)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt', # 添加版本文件
    icon=['display.ico'], # 添加Icon
)
