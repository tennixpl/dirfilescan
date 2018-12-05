import logging

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

    # scan

    try:
        worddoc = open(path + '/' + name, 'r')

    except FileNotFoundError:
        logger.error(f"file not found error for word doc {path}/{name}")
    finally:
        try: # There should be a better way to do this
            worddoc.close()
        except:
            None
