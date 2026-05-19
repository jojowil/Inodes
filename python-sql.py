import sys

# reads a redirected file and cuts it up from the form:
#  path|inode|parentinode|mode|type

'''
create database ciss110p8;

use ciss110p8;

create table entries(
    name varchar(255)
    , inode int unique
    , pinode int
    , mode smallint
    , type enum('f', 'd')
);

create user 'ciss110p8'@'%' identified by 'ciss110p8';

grant select on ciss110p8.* to 'ciss110p8'@'%';
'''

for line in sys.stdin:
    line = line.strip()
    parts = line.split("|")
    inode = parts[1]
    # inode 2 is the root directory
    file = "/" if inode == 2 else parts[0].split("/")[-1]
    pinode = parts[2]
    perms = parts[3]
    ftype = parts[4]

    # Inode 1 is reserved for the bad-block map and will be duplicated.
    # They may also be used for /proc and /sys, etc.
    if inode != '1' and pinode != '1':
        print(f"insert into entries values ('{file}',{inode},{pinode},{perms},'{ftype}');")
