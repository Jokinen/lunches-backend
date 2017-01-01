# -*- coding: utf-8 -*-

import sys
import logging
import logging.config

from __init__ import __version__
from sodexo import Sodexo
from unica import Unica

from db_manager import DB_manager


def main(argv):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(" {0}".format(__name__))

    logger.info(" Mobileparser version " + __version__)

    dbm = DB_manager()

    parsers = {}
    parsers["unica"] = Unica()
    # parsers["sodexo"] = Sodexo()

    try:
        dbm.init_db()
    except Exception, e:
        logger.exception(e)
        sys.exit(1)

    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        try:
            if arg in parsers:
                data = parsers[arg].parse()
                dbm.handle_data(data)
            else:
                logger.warning(" No parsers exist for key " + arg)
        except Exception, e:
            logger.exception(e)
            dbm.close_db()
            sys.exit(1)
    else:
        try:
            for key, parser in parsers.iteritems():
                data = parser.parse()
                dbm.handle_data(data)
        except Exception, e:
            logger.exception(e)
            dbm.close_db()
            sys.exit(1)

    try:
        dbm.update_parser_version(__version__)
        dbm.close_db()
        logger.info(" Parse complete")
    except Exception, e:
        logger.exception(e)
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv)
