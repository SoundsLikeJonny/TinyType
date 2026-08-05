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

import subprocess
from datetime import datetime
from pathlib import Path

command = Path().absolute().joinpath( 'venv/Scripts/pyinstaller.exe')
print(command)
print(command)
windowed = '--w'
args = str(Path.joinpath(Path().absolute(), 'build.spec'))

current_date_time = '\n\n\nNEW BUILD STARTED\n=========\n' + str(
    datetime.now().strftime("%d %B, %Y %H:%M,%S")) + '\n\n\n'

err = open('build_log.txt', 'a')
err.write(current_date_time)
err.flush()

print([command, windowed, args])

c = subprocess.Popen([command, args], stderr=err, shell=True, close_fds=True, universal_newlines=True)
print(str(c))
c.wait()
