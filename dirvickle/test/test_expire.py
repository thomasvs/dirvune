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

        self.assertEquals(len(ret), 21)


class ExpirerTestCase(unittest.TestCase):

    def setUp(self):
        testdir = os.path.dirname(__file__)
        self.expirer = expire.Expirer(os.path.join(testdir, 'master.conf'),
            os.path.join(testdir, 'vault'))


    def testGetImages(self):
        result = self.expirer.getImages()

        keep = [i for i in result if i[1] == 'keep']
        delete = [i for i in result if i[1] == 'delete']

        #self.assertEquals(len(result), 57)
        #self.assertEquals(len(keep), 21)
        #self.assertEquals(len(delete), 36)

        #self.assertEquals(keep[0][0], '20111011030000')
        #self.assertEquals(keep[-1][0], '20130323030000')

        #self.assertEquals(delete[0][0], '20111111030000')
        #self.assertEquals(delete[-1][0], '20130312030000')

        import pprint
        pprint.pprint(result)

        print "rm %s" % " ".join([d[0] for d in delete])

