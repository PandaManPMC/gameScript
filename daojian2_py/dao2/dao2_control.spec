# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['dao2_control.py'],
    pathex=[],
    binaries=[],
    datas=[('img/*', 'img'), ('paddle_ocr_models', 'paddle_ocr_models'), ('D:\\a\\codes\\game_script\\pythonProject\\.venv\\Lib\\site-packages\\paddleocr', './paddleocr'), ('D:\\a\\codes\\game_script\\pythonProject\\.venv\\Lib\\site-packages\\paddle', './paddle')],
    hiddenimports=['shapely.geometry', 'numpy', 'cv2', 'PIL', 'yaml', 'requests', 'tqdm', 'scipy', 'pyclipper', 'skimage', 'flask', 'chardet', 'nltk', 'skimage', 'skimage.morphology', 'skimage.morphology._skeletonize', 'imgaug', 'albumentations', 'docx', 'lxml'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='dao2_control',
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
    uac_admin=True,
)
