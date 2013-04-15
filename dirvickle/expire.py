# -*- Mode: Python; test-case-name: dirvickle.test.test_expire -*-
# vi:si:et:sw=4:sts=4:ts=4

import re
import time
import datetime

from dirvickle import expirerule, vault

_SECTION_RE = re.compile(r'^(?P<section>\S*):')

states = ['CONFIG', 'EXPIRERULE']

class Parser(object):

    def __init__(self, output):
        self._state = None
        self.rules = expirerule.Rules()


        lines = output.split('\n')

        for line in lines:
            if not line:
                continue
            if line.startswith('#'):
                continue

            m = _SECTION_RE.search(line)
            if m:
                section = m.group('section')
                if section == 'expire-rule':
                    self._state = 'EXPIRERULE'
                else:
                    self._state = 'CONFIG'
                continue

            if self._state == 'EXPIRERULE':
                self.rules.add(line)


class Expirer(object):

    def __init__(self, config, vaultPath):
        handle = open(config)
        output = handle.read()
        handle.close()

        self.parser = Parser(output)
        self.vault = vault.Vault(vaultPath)

    def _strToDateTime(self, text):
        t = time.strptime(text, "%Y%m%d%H%M%S")
        dt = datetime.datetime.fromtimestamp(time.mktime(t))
        return dt

    def getImages(self):
        """
        @rtype: list of name, decision, reason
        """
        got = self.vault.getImages()
        print got
        result = []

        first = self._strToDateTime(got[0])
        last = self._strToDateTime(got[-1])

        desired = self.parser.rules.getImages(first, last)

        # always keep the first one we have
        result.append([got[0], 'keep', 'first one is always kept'])
        del got[0]

        j = 0
        d = None

        for i, g in enumerate(got):
            if not d:
                (d, rules) = desired.pop(0)
                j += 1

            if g < d:
                result.append([g, 'delete',
                    'not needed for desired %d at %s' % (j, d)])
                print result[-1]
            else:
                diff = self._strToDateTime(g) - self._strToDateTime(d)
                result.append([g, 'keep', 'for desired %s with delta %s' % (
                    d, diff)])
                print result[-1]
                d = None

        return result
