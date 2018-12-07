###
# Set up a file scan of a directory
# inputs, directory to scan,

###

import os.path, sys, re
from argparse import ArgumentParser
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Get the 'plugins'
sys.path.append(f"{os.path.realpath(__file__).rsplit ('/', 1)[0]}/scanners/")


import text


def _txt(path, filename, dwlist):
    print("_txt")
    text.scan_file(path, filename, dwlist)


scanners = {
    'txt': _txt
}




#######################################################################################################################


def create_parser():
    parser: ArgumentParser = ArgumentParser(description="""
    Scan a directory, inspect each file for a list of forbidden terms
    """)
    parser.add_argument("-d", "--dir", help="Directory to scan, full path works best", required=False)
    parser.add_argument("-r", "--recursive_depth", type=int, help="Recursive depth of directories to scan", default=-1, required=False)
    parser.add_argument("-e", "--exclude", help="File types to exclude, comma separated list", required=False)
    parser.add_argument("-c", "--config", help="config json file with bad words", default="dirtywords.json", required=False)
    return parser

#######################################################################################################################


def validate_args():
    ###
    # Validate all args in arg parse
    ###

    validated_good = True

    # Validate file exclude list
    # Any possible exploits to happen here?

    if args.exclude != None:
        file_extensions = args.exclude.split(',')

        for ex in file_extensions:
            if ex[0] == '.':
                excludeList.append(ex[1:])
            else:
                excludeList.append(ex)
    # anything tha would actually fail? --tennixpl
    # ------------------------------------------------------------------------------------------------------------------
    # Validate file exists
    if os.path.isfile(args.config):
        logger.info("Config File Exists")
    else:

        validated_good = False
        print(f"{args.config} file given for config doesnt exist")
        logger.error(f"Config file {args.config} is not reachable in current path '{os.path.abspath(__file__)}'")
    # ------------------------------------------------------------------------------------------------------------------
    # Validate dir
    if os.path.isdir(args.dir):
        logger.info("Given directory exists")
    else:
        validated_good = False
        print(f"'{args.dir}' directory given for dir doesnt exist or is not accessible by user '{os.getlogin()}' ")
        logger.error(f"Directory'{args.dir}' doesn't exist or is not reachable by '{os.getlogin()}'")
    # ------------------------------------------------------------------------------------------------------------------
    # Validate depth

    if int(args.recursive_depth) >= -1:
        logger.info(f"Recursive Depth of {args.recursive_depth} is validated")
    else:
        validated_good = False
        print(f"Recursive depth '{args.recursive_depth}' is not valid, must be bigger than -1, -1 means full depth.")
        print("Resetting recursive depth to -1")
        args.recursive_depth = -1

    return validated_good

#######################################################################################################################

def directory_crawler(path, recursionsleft):
    filenamelist =[]
    dirnamelist = []

    print(path)
    nameslist = os.listdir(str(path))
    print(nameslist)

    logger.info(f"List of found file names {nameslist}")

    for name in nameslist:
        pathname = path + '/' + name
        if os.path.islink(pathname):
            logger.info("We do not follow symlinks, we want to avoid infinite recursions")
        elif os.path.isfile(pathname):
            filenamelist.append(name)
        elif os.path.isdir(pathname):
            dirnamelist.append(name)
        else:
            logger.info(f"'{name}' in {path} is not a file or directory...skipping")

    scanfiles(path, filenamelist)

    if recursionsleft > 0:
        for dirname in dirnamelist:
            directory_crawler(dirname, recursionsleft-1)
    elif recursionsleft == -1:
        for dirname in dirnamelist:
            directory_crawler(dirname, recursionsleft)
    else:
        logger.error("Something is very wrong with recursion number")
        sys.exit


#######################################################################################################################


def scanfiles(path, filenamelist):
    dws_found = []
    for filename in filenamelist:
        if filename.split('.')[-1] in scanners:
            dws_found.append(scanners[(filename.split('.')[-1])](path, filename, dwlist))

    print(dws_found)


#######################################################################################################################


def load_dirtywords():
    global dwlist
    dwlist=[]

    dwlist.append("[bB][oO][bB]")
    dwlist.append("mizlud")


#######################################################################################################################


def main():
    global args
    global excludeList
    excludeList = []

    args = create_parser().parse_args()
    validate_args()
    load_dirtywords()
    directory_crawler(args.dir, args.recursive_depth)

#######################################################################################################################


if __name__ == "__main__":
    main()
else:
    print("test")
