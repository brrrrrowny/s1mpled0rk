# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['dorksearch.py'],
             pathex=[],
             binaries=[],
             datas=[('fonts', 'pyfiglet/fonts')],
             hiddenimports=['pyfiglet.fonts'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

icon_path = 'icon.ico'
exe = EXE(pyz=a.pure,
          a=pyz,
          icon=icon.ico,  
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='S1MPLED0RK_by_Browny59',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
