# -*- Mode: Python; test-case-name: dirvickle.test.test_expire -*-
# vi:si:et:sw=4:sts=4:ts=4


import os
import datetime

import unittest

from dirvickle import expire


class ParserTestCase(unittest.TestCase):

    def setUp(self):
        handle = open(os.path.join(os.path.dirname(__file__), 'master.conf'))
        config = handle.read()
        handle.close()

        self.parser = expire.Parser(config)

    def testParser(self):
        ret = self.parser.rules.getImages(
            first=datetime.datetime(2012, 6, 1),
            last=datetime.datetime(2012, 11, 1),
            today=datetime.datetime(2012, 11, 11))

        print ret

