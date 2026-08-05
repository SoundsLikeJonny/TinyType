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

import glob
import os
from pathlib import Path


def main():
    """
    Creates the PySide6 Python UI files from .ui files
    Created in UCS Voice Naming Tool\\src\\ui\\gui
    """

    path_to_gui = Path().joinpath(os.getcwd(), 'generated')

    print(f"""
    #################
    #################
    #################
    #################

    {path_to_gui}

    #################
    #################
    #################
    #################
    """)

    for file in glob.glob(f"{path_to_gui}\\*.ui"):
        py_filename = Path(f'{path_to_gui}{file}').stem
        py_filepath = Path(f'{path_to_gui}\\{py_filename}.py')
        os.system(f'pyside6-uic "{file}" -o "{py_filepath}"')


if __name__ == "__main__":
    main()
