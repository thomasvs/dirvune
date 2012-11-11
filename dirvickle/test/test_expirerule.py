# -*- Mode: Python; test-case-name: dirvickle.test.test_expirerule -*-
# vi:si:et:sw=4:sts=4:ts=4

import datetime
import unittest

from dirvickle import expirerule



class RuleTestCase(unittest.TestCase):

    def testRule(self):
       rule = expirerule.Rule('* * * * sat +3 months')
       self.assertEquals(rule.dom, '*')
       self.assertEquals(rule.strftime, '+3 months')


class RulesTestCase(unittest.TestCase):


    def testEverySat3Months(self):
        rules = expirerule.Rules()
        rules.add('* * * * sat +3 months')
        ret = rules.getImages(
            first=datetime.datetime(2012, 6, 1),
            last=datetime.datetime(2012, 11, 1),
            today=datetime.datetime(2012, 11, 11))

        self.assertEquals(len(ret), 12)
        self.assertEquals(ret[0][0], '20120811000000')

    def testEveryFirst3Months(self):
        rules = expirerule.Rules()
        rules.add('* * 1 * * +3 months')
        ret = rules.getImages(
            first=datetime.datetime(2012, 6, 1),
            last=datetime.datetime(2012, 11, 1),
            today=datetime.datetime(2012, 11, 11))

        self.assertEquals(len(ret), 3)
        self.assertEquals(ret[0][0], '20120901000000')

    def testEveryOctoberDay3Months(self):
        rules = expirerule.Rules()
        rules.add('* * * oct * +3 months')
        ret = rules.getImages(
            first=datetime.datetime(2012, 6, 1),
            last=datetime.datetime(2012, 11, 1),
            today=datetime.datetime(2012, 11, 11))

        self.assertEquals(len(ret), 31)
        self.assertEquals(ret[0][0], '20121001000000')

    def testEveryOctoberSat3Months(self):
        rules = expirerule.Rules()
        rules.add('* * * oct sat +3 months')
        ret = rules.getImages(
            first=datetime.datetime(2012, 6, 1),
            last=datetime.datetime(2012, 11, 1),
            today=datetime.datetime(2012, 11, 11))

        self.assertEquals(len(ret), 4)
        self.assertEquals(ret[0][0], '20121006000000')


    def testEverySatNever(self):
        rules = expirerule.Rules()
        rules.add('* * * * sat never')
        ret = rules.getImages(
            first=datetime.datetime(2012, 6, 1),
            last=datetime.datetime(2012, 11, 1),
            today=datetime.datetime(2012, 11, 11))

        self.assertEquals(len(ret), 22)
        self.assertEquals(ret[0][0], '20120602000000')


class MyRulesTestCase(unittest.TestCase):

    def testMine(self):
        rules = expirerule.Rules()
        rules.add('* * * * sat +3 months')
        rules.add('* * 1-7 * sat +1 year')
        rules.add('* * 1-7 1,4,7,10 sat never')
        ret = rules.getImages(
            first=datetime.datetime(2011, 10, 11),
            last=datetime.datetime(2012, 11, 10),
            today=datetime.datetime(2012, 11, 11))

        self.assertEquals(len(ret), 23)
        self.assertEquals(ret[0][0], '20111203000000')
        self.failUnless(len(ret[0][1]), 1)
        self.failUnless(ret[0][1][0].endswith('year'))
        # second one has 2 reasons
        self.assertEquals(len(ret[1][1]), 2)
        self.failUnless(ret[1][1][1].endswith('never'))
        # some other one has 3 reasons
        self.assertEquals(len(ret[17][1]), 3)
        self.assertEquals(ret[17][0], '20121006000000')
