import logging
import re

logger = logging.getLogger(__name__)


def scan_word_doc(path, name, dwlist):
    """
    Scan a provided word doc
    :param path:
    :param name:
    :param dwlist:
    :return: list of words found in document and number of occurrences
    """

    logger.info("Scanning word Doc")
    worddoc_lines =[]
    found = []

    # scan

    try:
        worddoc = open(path + '/' + name, 'r')
        worddoc_lines = worddoc.readlines()
        worddoc.close()
    except FileNotFoundError:
        logger.error(f"file not found error for word doc {path}/{name}")
        raise FileNotFoundError
    finally:
        try: # There should be a better way to do this
            worddoc.close()
        except:
            None

    for line in file_lines:
        for dw in dwlist:

            if re.findall(dw, line, re.IGNORECASE) != []:
                found.append(dw)

    # TODO Delete me and make a proper log
    print(f"The found words are {found}")