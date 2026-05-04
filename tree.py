import os
import stat
import sys

def get_file_type_char(mode):
    # returns a letter representing the type. symlink is checked first.
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


def print_directory_tree_with_inodes(path='.'):
    # print file, inode, parent inode, mode, and type recursively.
    # TODO clean this up a bit more.
    try:
        # Get stats for the root directory itself
        root_stat = os.stat(path)
        root_inode = root_stat.st_ino
        root_parent_inode = os.stat(os.path.dirname(path)).st_ino if os.path.dirname(path) else None
        root_perms = oct(root_stat.st_mode)[-3:]
        ftype = get_file_type_char(root_stat.st_mode)

        #print(f"{'Path':<40} {'Inode':<12} {'Parent Inode':<12} {'Perms'}")
        #print("-" * 80)
        #print(f"{path:<40} {root_inode:<12} {root_parent_inode or 'None':<12} {root_perms} {type}")
        print(f"{path}|{root_inode}|{root_parent_inode or 'None'}|{root_perms}|{ftype}")

        for root, dirs, files in os.walk(path):
            # Process directories first to show hierarchy
            for name in dirs:
                full_path = os.path.join(root, name)
                try:
                    if os.path.islink(full_path):
                        continue
                    stat_info = os.stat(full_path)
                    parent_stat = os.stat(root)
                    ftype = get_file_type_char(stat_info.st_mode)

                    #print(f"{full_path:<40} {stat_info.st_ino:<12} {parent_stat.st_ino:<12} {oct(stat_info.st_mode)[-3:]} {type}")
                    if type != "l":
                        print_directory_tree_with_inodes(full_path)
                    else:
                        print(f"{full_path}|{stat_info.st_ino}|{parent_stat.st_ino}|{oct(stat_info.st_mode)[-3:]}|{ftype}")
                except PermissionError:
                    print(f"{full_path:<40} {'Permission Denied':<12} {'':<12} {'':<5}")

            # Process files
            for name in files:
                full_path = os.path.join(root, name)
                try:
                    if os.path.islink(full_path):
                        continue
                    stat_info = os.stat(full_path)
                    parent_stat = os.stat(root)
                    ftype = get_file_type_char(stat_info.st_mode)

                    #print(f"{full_path:<40} {stat_info.st_ino:<12} {parent_stat.st_ino:<12} {oct(stat_info.st_mode)[-3:]} {type}")
                    print(f"{full_path}|{stat_info.st_ino}|{parent_stat.st_ino}|{oct(stat_info.st_mode)[-3:]}|{ftype}")
                except PermissionError:
                    print(f"{full_path:<40} {'Permission Denied':<12} {'':<12} {'':<5}")

    except FileNotFoundError:
        print(f"Error: The path '{path}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied accessing '{path}'.")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Change this to any directory you want to inspect
        target_dir = input("Enter directory path (press Enter for current dir): ").strip()
        if not target_dir:
            target_dir = '.'
    else:
        target_dir = sys.argv[1]

    print_directory_tree_with_inodes(target_dir)
