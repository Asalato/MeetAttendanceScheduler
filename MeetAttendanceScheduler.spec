# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
home = str(Path.home())
block_cipher = None

a = Analysis(['MeetAttendanceScheduler.py'],
             pathex=[home + '\\GitHub\\MeetAttendanceScheduler'],
             binaries=[(home + '\\GitHub\\MeetAttendanceScheduler\chromedriver.exe', '.\\')],
             datas=[(home + '\\anaconda3\\lib\\site-packages\\eel\\eel.js', 'eel'), ('web', 'web')],
             hiddenimports=['bottle_websocket'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['numpy', 'pandas'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='MeetAttendanceScheduler',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
