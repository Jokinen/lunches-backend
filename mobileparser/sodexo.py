# -*- coding: utf-8 -*-

__version__ = '0.1.0'

import logging
from bs4 import BeautifulSoup as bs
from parser_abc import Parser, Restaurant, Day, Food


class Sodexo(Parser):
    # @abstractmethod
    def __init__(self):
        super(Sodexo, self).__init__("Sodexo", __version__)
        self.logger = logging.getLogger(" {0}".format(__name__))

    # @abstractmethod
    def parse(self):
        raise Exception("not implemented yet")

    # @abstractmethod
    def parse_page(self, page):
        raise Exception("not implemented yet")

    def __repr__(self):
        return "{0} version {1}".format(self.name, __version__)
