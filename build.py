#      TinyType is a minimal typing test software that sits in the corner of your screen while you work!
#      Copyright (C) 2026  Jon Evans
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
