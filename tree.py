import os
import stat
import sys

def get_file_type_char(mode):
    if stat.S_ISLNK(mode):
        return 'l'
    elif stat.S_ISDIR(mode):
        return 'd'
    elif stat.S_ISREG(mode):
        return 'f'
    elif stat.S_ISBLK(mode):
        return 'b'
    elif stat.S_ISCHR(mode):
        return 'c'
    elif stat.S_ISFIFO(mode):
        return 'p'
    elif stat.S_ISSOCK(mode):
        return 's'
    else:
        return '?'


def print_files(path):
    # Get files from a directory path - unconfirmed path as dir
    try:
        root, dirs, files = list(os.walk(path))[0]
        # Process files
        for name in files:
            full_path = os.path.join(root, name)
            try:
                # no symlinks
                if os.path.islink(full_path):
                    print(f"{full_path} is a symlink. Skipping.", file=sys.stderr)
                    continue

                ftype = get_file_type_char(os.stat(full_path).st_mode)
                if ftype == 'f':
                    print_formatted_path(full_path)
            except PermissionError:
                print(f"{full_path:<40} {'Permission Denied':<12} {'':<12} {'':<5}", file=sys.stderr)
    except FileNotFoundError:
        print(f"Error: The path '{path}' was not found.", file=sys.stderr)
    except PermissionError:
        print(f"Error: Permission denied accessing '{path}'.", file=sys.stderr)


def print_formatted_path(path):
    try:
        # Get stats for the path
        root_stat = os.stat(path)
        parent_stat = os.stat(os.path.dirname(path))
        ftype = get_file_type_char(root_stat.st_mode)
        print(f"{path}|{root_stat.st_ino}|{parent_stat.st_ino}|{oct(root_stat.st_mode)[-3:]}|{ftype}")
    except FileNotFoundError:
        print(f"Error: The path '{path}' was not found.", file=sys.stderr)
    except PermissionError:
        print(f"Error: Permission denied accessing '{path}'.", file=sys.stderr)


def print_directory_tree_with_inodes(path):
    try:
        root, dirs, files = list(os.walk(path))[0]
        #print_formatted_path(root)
        #print(f"pdtwi called with {root}")
        for name in dirs:
            full_path = os.path.join(root, name)
            try:
                if os.path.islink(full_path):
                    continue
                else:
                    ftype = get_file_type_char(os.stat(full_path).st_mode)
                    if ftype == 'd':
                        print_formatted_path(full_path)
                        print_directory_tree_with_inodes(full_path)
                        print_files(full_path)
            except PermissionError:
                print(f"{full_path:<40} {'Permission Denied':<12} {'':<12} {'':<5}", file=sys.stderr)
    except FileNotFoundError:
        print(f"Error: The path '{path}' was not found.", file=sys.stderr)
    except PermissionError:
        print(f"Error: Permission denied accessing '{path}'.", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        target_dir = input("Enter directory path (press Enter for current dir): ").strip()
        if not target_dir:
            print("\nYou must provide a path intractively or on the command line.\n", file=sys.stderr)
            sys.exit(1)
    else:
        target_dir = sys.argv[1]

    print_formatted_path(target_dir)
    print_directory_tree_with_inodes(target_dir)
