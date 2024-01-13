import os
import sys
import json
import pathlib
import argparse
# import pprint

def parse_arguments():
    parser = argparse.ArgumentParser(description="find a file or folder in your file system")
    parser.add_argument('-f', required=True, help="The file/folder you are trying to search for")
    parser.add_argument('-s', default=os.getcwd(), required=False, help="Where do you want to try and find your file?")
    parser.add_argument('-c', default="config.json", help="The location of the config (json) file, if not specified the program will look for a file called 'config.json' in the current directory")
    args = parser.parse_args()
    if not os.path.exists(args.c):
        print("Could not find config.json, try specifying one with -c")
        sys.exit(1)
    return args
    


def print_list(l):
    for item in l:
        print(item)

def read_json(path):
    with open(path, "r") as fh:
        content = json.load(fh)

    return content

def is_eligible(target, cur_dir):
    return target in cur_dir.lower()

def search_for(find, start, ignore=[], ignore_dots=False, _res=None):
    if _res == None:
        _res = []
    
    for dir in os.listdir(start):
        cur_dir = os.path.join(start, dir)
        # print(dir)
        if dir in ignore:
            continue
        elif dir.startswith('.') and ignore_dots:
            continue
        elif is_eligible(find, dir):
            _res.append(cur_dir)
        elif os.path.isdir(cur_dir):
            search_for(find, cur_dir, ignore, ignore_dots, _res)
        
    return _res

if __name__ == "__main__":
    args = parse_arguments()
    config = read_json(args.c)
    start_dir = args.s
    find_dir = args.f
    print(f"\nFOUND:")
    print_list(search_for(find_dir, start_dir, ignore=config["ignore"], ignore_dots=config["ignore_dots"]))
    # print(read_json())