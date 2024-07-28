import os

# Define the license comment block to be removed
license_comment_block = """
#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of Pyrofork.
#
#  Pyrofork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrofork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrofork.  If not, see <http://www.gnu.org/licenses/>.
"""


def remove_license(file_path):
    with open(file_path) as file:
        content = file.read()

    # Remove the specific license comment block
    updated_content = content.replace(
        license_comment_block.strip(), ""
    ).strip()

    with open(file_path, "w") as file:
        file.write(updated_content)


def remove_from_repo(repo_path):
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                remove_license(file_path)

if __name__ == "__main__":
    # Path to the specific directory you want to process
    repo_path = "."
    remove_from_repo(repo_path)
