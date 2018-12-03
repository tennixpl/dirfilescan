###
# Set up a file scan of a directory
# inputs, directory to scan,

###

import os.path
from argparse import ArgumentParser
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_parser():
    parser: ArgumentParser = ArgumentParser(description="""
    Scan a directory, inspect each file for a list of forbidden terms
    """)
    parser.add_argument("-d", "--dir", help="Directory to scan, full path works best", required=False)
    parser.add_argument("-r", "--recursive_depth", type=int, help="Recursive Depth", default=-1, required=False)
    parser.add_argument("-e", "--exclude", help="File types to exclude, comma sep list", required=False)
    parser.add_argument("-c", "--config", help="config json file with bad words", default="dirtyword.json", required=False)
    return parser


def validate_args():
    ###
    # Validate all args in arg parse
    ###

    validated_good = True


    # Validate file exclude list
    # Any possible exploits to happen here?

    file_extensions = args.exclude.split(',')

    for ex in file_extensions:
        if ex[0] == '.':
            excludeList.append(ex[1:])
        else:
            excludeList.append(ex)
    # anything tha would actually fail? --tennixpl

    # Validate file exists
    if os.path.isfile(args.config):
        logger.info("Config File Exists")
    else:
        validated_good = False
        print(f"{args.config} file given for config doesnt exist")
        logger.error(f"Config file {args.config} is not reachable in current path '{os.path.abspath(__file__)}'")

    # Validate dir
    if os.path.isdir(args.dir):
        logger.info("Given directory exists")
    else:
        validated_good = False
        print(f"'{args.dir}' directory given for dir doesnt exist or is not accessible by user '{os.getlogin()}' ")
        logger.error(f"Directory'{args.dir}' doesn't exist or is not reachable by '{os.getlogin()}'")

    # Validate depth

    if int(args.recursive_depth) >= -1:
        logger.info(f"Recursive Depth of {args.recursive_depth} is validated")
    else:
        validated_good = False
        print(f"Recursive dpeth '{args.recursive_depth}' is not valid, must be bigger than -1, -1 means full depth.")
        print("Resetting recursive depth to -1")
        args.recursive_depth = -1

    return validated_good


def main():
    global args
    global excludeList
    excludeList = []

    args = create_parser().parse_args()
    validate_args()

    print(args)


if __name__ == "__main__":
    main()
else:
    print("test")
