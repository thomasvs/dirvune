# -*- Mode: Python; test-case-name: dirvune.test.test_expirerule -*-
# vi:si:et:sw=4:sts=4:ts=4



import string
import datetime

from dirvune import perl

def dt2e(dt):
    return int(dt.strftime("%s"))

class Rule:

    def __init__(self, description):
        self.description = description
        (min, hr, self.dom, self.mon, self.dow, self.strftime) = string.split(
            description, maxsplit=5)

        # the perl code changes , to space so that Time::Period can parse it
        for attr in ['dom', 'mon', 'dow']:
            setattr(self, attr, getattr(self, attr).replace(',', ' '))

class Rules(object):
    """
    I contain dirvish expiry rules.
    """

    def __init__(self):
        self._rules = []

    def add(self, description):
        """
        @type description: C{str}
        """
        self._rules.append(Rule(description))

    def match(self, perler, current, text, format):
        if text == '*':
            return True

        ret = perler.inPeriod(dt2e(current), format % text)
        if ret == -1:
            print 'WARNING: could not parse %s' % text
        return ret == 1


    def getImages(self, first, last, today=None):
        """
        Get all image directories we should have according to expire rules,
        between the given first and last dates, as seen from today.

        @type first: C{datetime.datetime}

        @rtype:   list of (str, list of str)
        @returns: list of datestring, rule descriptions
        """

        if not today:
            today = datetime.datetime.now()

        ret = {}

        perler = perl.Perl()
        perler.start()

        for rule in self._rules:
            timedelta = None
            # hacky way to get the delta from the last item in the expire-rule
            if rule.strftime != 'never':
                epoch = perl.parsedate(rule.strftime, dt2e(today))
                timedelta = datetime.datetime.fromtimestamp(epoch) - today
                since = today - timedelta
                until = last
            else:
                since = first
                until = last


            current = since
            while current <= until:
                value = current.strftime("%Y%m%d000000")

                match = True

                if not self.match(perler, current, rule.dom, "md {%s}"):
                    match = False

                if not self.match(perler, current, rule.mon, "mo {%s}"):
                    match = False

                if not self.match(perler, current, rule.dow, "wd {%s}"):
                    match = False

                if match:
                    value = current.strftime("%Y%m%d000000")
                    if value not in ret:
                        ret[value] = []
                    ret[value].append(rule.description)

                current += datetime.timedelta(days=1)

        perler.stop()
        ret = ret.items()
        ret.sort()
        return ret
