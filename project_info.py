#  Copyright (c) 2026 Jon Evans
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

import dataclasses


@dataclasses.dataclass
class Info:
    NOTIFICATION_TIME: int = 50
    PROJECT_TITLE: str = 'TinyType'
    COMPANY: str = 'Jon Evans'
    COPYRIGHT: str = 'Copyright (c) Jon Evans 2026'
    NOTICE: str = 'Tiny but powerful!'
    RESOURCES_PATH: str = 'resources'
    ICON_PATH: str = f':/{RESOURCES_PATH}/favicon.png'
    SPLASH_PATH: str = f':/{RESOURCES_PATH}/splash.png'
    DOCS_LINK: str = ''



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
