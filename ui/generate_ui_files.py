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
