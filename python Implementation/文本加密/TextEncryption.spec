# -*- mode: python ; coding: utf-8 -*-


block_cipher = pyi_crypto.PyiBlockCipher(key='X?44tNJ!Umu!WbY6b!dF2C2-zjZ?9N5r5l-!-q1pu-m9-9tqB0JRa?n!m!pn!-BD-nEbsm6JQlmOf-P56ng2?Lq8?3?!f9f?ZpKG')


a = Analysis(
    ['TextEncryption.pyw'],
    pathex=[],
    binaries=[],
    datas=[('encrypted.ico', '.')],
    hiddenimports=[],
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
    name='TextEncryption',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['encrypted.ico'],
)
