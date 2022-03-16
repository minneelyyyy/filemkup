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
        "show_all": False,
        "directory": "",
        "minimum_percent": 1.00,
    }

    skip = False

    for i in range(len(args)):
        if skip:
            skip = False
            continue

        if args[i] in ("--dont-print-bar", "-b"):
            ret["print_bar"] = False
        elif args[i] in ("--dont-print-percent", "-p"):
            ret["print_percent"] = False
        elif args[i] in ("--show-all", "-A"):
            ret["show_all"] = True
        elif args[i] in ("--minimum", "-m"):
            ret["minimum_percent"] = args[i + 1]
            skip = True
        else:
            if os.path.exists(args[i]):
                if os.path.isdir(args[i]):
                    ret["directory"] = args[i]
                else:
                    print(f"filemkup: error: \"{args[i]}\" is not a directory")
                    exit(1)
            else:
                print(f"filemkup: error: \"{args[i]}\" does not exist")
                exit(1)

    if not ret["directory"]:
        ret["directory"] = os.getenv("PWD")

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

    
    def get_percent_bar(percent, max_len):
        # subtract 2 to account for [ and ]
        max_len -= 2

        if options["print_bar"]:
            return f"[\033[33;1m{'=' * int(max_len * percent)}\033[0m" \
                f"{' ' * (max_len - int(max_len * percent))}] "
        
        return ""


    def get_percent(percent):
        if options["print_percent"]:
            return f"\033[1m{percent * 100:5.2f}% \033[0m"
        
        return ""


    for ext, cnt in extensions:
        if not options["show_all"] and (cnt / total * 100) <= float(options["minimum_percent"]):
            continue

        string_after_percent_bar = f"{get_percent(cnt / total)}.{ext}"
        print(f"{get_percent_bar(cnt / total, 60)}{string_after_percent_bar}")


if __name__ == "__main__":
    main()
