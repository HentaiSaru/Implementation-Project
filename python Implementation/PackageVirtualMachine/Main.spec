# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(1000000000)

block_cipher = pyi_crypto.PyiBlockCipher(key='38697789753674')

a = Analysis(
    ["Start.pyw","GUIV\\ClickMain.py","GUIV\\InitialV.py","GUIV\\Secondaryfunction.py"],
    pathex=["C:\\GitHubProject\\Implementation Project\\python Implementation\\Virtual\\Scripts\\GUI Maker"],
    binaries=[],
    datas=[("GUIV\\click.ico", "GUIV")],
    hiddenimports=['cython', 'sklearn', 'sklearn.ensemble', 'sklearn.neighbors.typedefs', 'sklearn.neighbors.quad_tree', 'sklearn.tree._utils','sklearn.utils._cython_blas'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Main.exe',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_args = ['-9'],
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="C:\\GitHubProject\\Implementation Project\\python Implementation\\Virtual\\Scripts\\GUI Maker\\click.ico",
    onefile=True
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_args = ['-9'],
    upx_exclude=[],
    upx_debug_info=False,
    name='Main',
    onefile=True
)
