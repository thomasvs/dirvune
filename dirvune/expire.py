# -*- Mode: Python; test-case-name: dirvune.test.test_expire -*-
# vi:si:et:sw=4:sts=4:ts=4

import re
import time
import datetime

from dirvune import expirerule, vault

_SECTION_RE = re.compile(r'^(?P<section>\S*):\s*(?P<value>.*)$')

states = ['CONFIG', 'EXPIREDEFAULT', 'EXPIRERULE']

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
                elif section == 'expire-default':
                    self._state = 'EXPIREDEFAULT'
                    value = m.group('value')
                    self.rules.add('* * * * * %s' % value)
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
        @rtype: list of name, decision, list of reason
        """
        got = self.vault.getImages()
        result = []

        first = self._strToDateTime(got[0])
        last = self._strToDateTime(got[-1])

        desired = self.parser.rules.getImages(first, last)

        # always keep the first one we have
        result.append([got[0], 'keep', ['first one is always kept']])
        del got[0]

        j = 0
        d = None

        for i, g in enumerate(got):
            if not d:
                (d, rules) = desired.pop(0)
                j += 1

            if g < d:
                result.append([g, 'delete',
                    ['not needed for desired %d at %s' % (j, d)]])
            else:
                diff = self._strToDateTime(g) - self._strToDateTime(d)
                result.append([g, 'keep', ['for desired %s with delta %s' % (
                    d, diff)]])

                # skip through desireds as long as our got is later
                while g >= d and desired:
                    (d, rules) = desired.pop(0)
                    diff = self._strToDateTime(g) - self._strToDateTime(d)
                    result[-1][2].append(['for desired %s with delta %s' % (
                        d, diff)])
                    if not desired:
                        break

        return result