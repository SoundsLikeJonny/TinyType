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

import dataclasses


@dataclasses.dataclass
class Info:
    NOTIFICATION_TIME: int = 50
    PROJECT_TITLE: str = 'TinyType'
    COMPANY: str = 'Jon Evans'
    COPYRIGHT: str = 'Copyright (c) Jon Evans 2026'
    NOTICE: str = 'Tiny but powerful!'
    RESOURCES_PATH: str = 'resources'
    ICON_PATH: str = f'{RESOURCES_PATH}/favicon.ico'
    SPLASH_PATH: str = f'{RESOURCES_PATH}/splash.png'
    DOCS_LINK: str = ''
    VERSION: str = '0.1.0-beta.5'
    GITHUB_REPO: str = 'SoundsLikeJonny/TinyType'



@dataclasses.dataclass
class FileTypes:
    PROJECT: str = '.tiny'
    DATA: str = '.tinydata'
    PREFS: str = '.tinyprefs'

    ALL_TYPES: tuple = (
        PROJECT,
        DATA,
        PREFS
    )

    @staticmethod
    def is_type_in_file(file: str):
        for extension in FileTypes.ALL_TYPES:
            if file.endswith(extension):
                return True
        return False
