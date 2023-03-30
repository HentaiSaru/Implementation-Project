# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(1000000000)

block_cipher = pyi_crypto.PyiBlockCipher(key='38697789753674')

a = Analysis(
    ['UPX.Py'],
    pathex=["R:\\wate\\"],
    binaries=[],
    datas=[("Compression.ico", ".")],
    hiddenimports=['cython', 'sklearn', 'sklearn.ensemble', 'sklearn.neighbors.typedefs', 'sklearn.neighbors.quad_tree', 'sklearn.tree._utils','sklearn.utils._cython_blas'],
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
    name='Compression',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_args = ['-9'],
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="R:\\wate\\Compression.ico",
)
