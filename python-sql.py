import sys

'''
create database hms;

use hms;

create table entries(
    name varchar(255)
    , inode int
    , pinode int
    , mode smallint
    , type enum('f', 'd')
);
'''

for line in sys.stdin:
    line = line.strip()
    parts = line.split("|")
    inode = parts[1]
    file = "/" if inode == '2' else parts[0].split("/")[-1]
    pinode = parts[2]
    perms = parts[3]
    ftype = parts[4]

    # Inode 1 is reserved for the bad-block map and will be duplicated.
    # They may also be used for /proc and /sys, etc.
    if inode != '1' and pinode != '1':
        print(f"insert into entries values ('{file}',{inode},{pinode},{perms},'{ftype}');")
