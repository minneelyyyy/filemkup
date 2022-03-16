#!/usr/bin/python3

import os
import sys

options = {
    "print_bar": True,
    "print_percent": True,
}


def parse_args(args):
    ret = {
        "print_bar": True,
        "print_percent": True,
        "directory": "",
    }

    for arg in args:
        if arg in ("--dont-print-bar", "-b"):
            ret["print_bar"] = False
        elif arg in ("--dont-print-percent", "-p"):
            ret["print_percent"] = False
        else:
            if os.path.exists(arg):
                if os.path.isdir(arg):
                    ret["directory"] = arg
                else:
                    print(f"filemkup: error: \"{arg}\" is not a directory")
                    exit(1)
            else:
                print(f"filemkup: error: \"{arg}\" does not exist")
                exit(1)
    
    return ret


def get_files(directory, files):
    for file in os.listdir(directory):
        if file[0] == '.':
            continue

        if os.path.isdir(f"{directory}/{file}"):
            get_files(f"{directory}/{file}", files)
        else:
            files.append(file)


def main():
    extensions: dict[str, int] = {}
    directory = os.getenv("PWD")
    files: list[str] = []
    options = parse_args(sys.argv[1:])

    get_files(options["directory"], files)

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

    total = 0

    for _, cnt in extensions:
        total += cnt

    
    def get_percent_bar(percent):
        if options["print_bar"]:
            return f"[\033[33;1m{'=' * int(40 * percent)}\033[0m{' ' * (40 - int(40 * percent))}] "
        
        return ""
    
    
    def get_percent(percent):
        if options["print_percent"]:
            return f"{percent * 100:5.2f}% "
        
        return ""


    for ext, cnt in extensions:
        if cnt / total < 0.01:
            continue

        print(f"{get_percent_bar(cnt / total)}\033[1m{get_percent(cnt / total)}\033[0m.{ext}")


if __name__ == "__main__":
    main()
