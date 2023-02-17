#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from os import listdir
from os.path import isfile
from os.path import join
from pathlib import Path
from typing import Set

import yaml
from more_itertools import flatten
from more_itertools import one


def files_in_folder(directory: str) -> Set[str]:
    dir_contents = listdir(directory)
    dir_files = filter(lambda entry: isfile(join(directory, entry)), dir_contents)
    return set(dir_files)


python_directory = "ra_utils"
markdown_directory = "docs/modules"

python_files = files_in_folder(python_directory)
python_files.remove("__init__.py")

# We want a markdown file for each python file
wanted_markdown_files = set(map(lambda file: file.replace(".py", ".md"), python_files))

actual_markdown_files = files_in_folder(markdown_directory)
mismatch = wanted_markdown_files.symmetric_difference(actual_markdown_files)
if mismatch:
    print("File mismatch between python code and module docs", mismatch)
    exit(1)

# Extract the filenames of modules in the nav in mkdocs
mkdocs_text = Path("mkdocs.yml").read_text()
mkdocs = yaml.safe_load(mkdocs_text)
nav = mkdocs["nav"]
dict_entries = filter(lambda entry: isinstance(entry, dict), nav)
dict_entries = filter(lambda entry: entry.keys() == {"Modules"}, dict_entries)
modules = one(dict_entries)["Modules"]
modules = flatten(map(lambda entry: entry.values(), modules))  # type: ignore
modules = set(map(lambda entry: entry[len("modules/") :], modules))  # type: ignore
# At this point modules is a set of filenames in the TOC

mismatch = modules.symmetric_difference(actual_markdown_files)
if mismatch:
    print("Mismatch between module docs and index", mismatch)
    exit(1)

exit(0)
