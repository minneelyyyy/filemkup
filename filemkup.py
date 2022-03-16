#!/usr/bin/python3

import os
import sys

files: list[str] = []
directory: str

if len(sys.argv) > 1:
    directory = sys.argv[1]
else:
    directory = os.getenv("PWD")


def get_files(directory):
    for file in os.listdir(directory):
        if file[0] == '.':
            continue

        if os.path.isdir(f"{directory}/{file}"):
            get_files(f"{directory}/{file}")
        else:
            files.append(file)


get_files(directory)

extensions: dict[str, int] = {}

for file in files:
    # skip files with no extension
    if not '.' in file:
        continue

    extension = file.split('.')[-1]

    if not extension in extensions:
        extensions[extension] = 0
    
    extensions[extension] += 1

# extensions gets converted into list[(str, int)]
extensions = sorted(list(extensions.items()), key=lambda x: x[1], reverse=True)

count = 0

for _, cnt in extensions:
    count += cnt

def get_percent_bar(percent):
    return f"[\033[33;1m{'=' * int(40 * percent)}\033[0m{' ' * (40 - int(40 * percent))}] "

for ext, cnt in extensions:
    if cnt / count < 0.01:
        continue

    print(f"{get_percent_bar(cnt / count)}\033[1m{(cnt / count) * 100:5.2f}%\033[0m .{ext}")
