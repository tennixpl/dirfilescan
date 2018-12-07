import re
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def scan_file(path, filename, dwlist):
    logger.info(f"looking in {path}")
    logger.info(f"for file {filename}")
    logger.info(f"With dirty words {dwlist}")

    found = []
    try:
        file_to_scan = open(path + '/' + filename, 'r')
        file_lines = file_to_scan.readlines()
        file_to_scan.close()

        line_in_file = 0
        for line in file_lines:
            #print(line)
            line_in_file += 1
            for dw in dwlist:
                if re.findall(dw, line, re.IGNORECASE):
                    #print("hit")
                    found.append([dw, line_in_file])
                    #print(found)

    except FileNotFoundError:
        logger.error(f"Issuing opening {filename}")
    finally:
        None

    print(found)
    return found