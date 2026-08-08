# -*- mode: python ; coding: utf-8 -*-
#  Copyright (c) 2024 Jon Evans.
#
#  The original Wwise-Python Tool Template and source code is provided by Jon Evans,
#  Copyright 2024 (c) Jon Evans Audio under the Apache License, Version 2.0
#  for the purposes of distributing internal tools
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# "C:\Users\jonev\PycharmProjects\wwise-ue-differ\.venv\Scripts\pyinstaller.exe" --windowed "C:\Users\jonev\PycharmProjects\wwise-ue-differ\build.spec"
# Icons: https://icons8.com/icon/set/folder-link/offices

import PyInstaller.config
from datetime import datetime
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from project_info import Info
try:
    import resources
except ImportError:
    pass


icon_name = str(Path.joinpath(Path().absolute(), 'resources', 'favicon.ico'))
print(f'icon_name: {icon_name}')

current_date_time = str(datetime.now().strftime("%Y_%m_%d-%H_%M_%S"))


buildnumber = str(datetime.now().strftime("%Y%m%d.%H%M%S"))
buildnumber = f'{Info.PROJECT_TITLE}\n' \
                f'{Info.COMPANY}\n'\
                f'{Info.COPYRIGHT}\n'\
                f'{Info.NOTICE}\n'\
                f'Build Date: {buildnumber}\n'\
                f'Author: Jon Evans'

try:
        with open('info.txt', 'w') as f:
                for line in buildnumber:
                        f.write(line)
except Exception as e:
        print(str(e))

if os.environ.get("CI"):
    workfolder = str(Path.joinpath(Path().absolute(), 'dist'))
    os.makedirs(workfolder, exist_ok=True)
else:
    parent_folder = str(Path.joinpath(Path().absolute(), 'builds', f'{Info.PROJECT_TITLE}_{current_date_time}'))
    workfolder = f'{parent_folder}'
    os.makedirs(workfolder)
    try:
        os.startfile(workfolder)
    except Exception:
        pass

PyInstaller.config.CONF['distpath'] = f"{workfolder}"

block_cipher = None

import glob
analysis_data = []
for path in glob.glob('.\\resources\\*.png'):
        analysis_data.append((path, '.\\resources\\'))

for path in glob.glob('.\\resources\\*.ico'):
        analysis_data.append((path, '.\\resources\\'))

# for path in glob.glob('./src/ui/gui/*.ui'):
#         analysis_data.append((path, './src/ui/gui/'))

analysis_data = analysis_data + [('./info.txt', './'), ('./LICENSE', './'), ('./README.md', './')]
print(analysis_data)

a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=analysis_data,
             hiddenimports=[],
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

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name=Info.PROJECT_TITLE,
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon=icon_name
          )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[], name=Info.PROJECT_TITLE)
