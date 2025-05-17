# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
	['main.py'],
	pathex=[],
	binaries=[],
	datas=[('hue_config.json', '.')],  # Include config file
	hiddenimports=['config_loader', 'hue_controller', 'gmail_monitor'],
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
	name='hue-email-automation',
	debug=False,
	bootloader_ignore_signals=False,
	strip=False,
	upx=True,
	upx_exclude=[],
	runtime_tmpdir=None,
	console=True,  # Set to False for no console window
	icon='NONE',
	disable_windowed_traceback=False,
	argv_emulation=False,
	target_arch=None,
	codesign_identity=None,
	entitlements_file=None,
)
