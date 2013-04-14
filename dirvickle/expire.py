# -*- Mode: Python; test-case-name: dirvickle.test.test_expire -*-
# vi:si:et:sw=4:sts=4:ts=4

import re

from dirvickle import expirerule

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
                print 'rule', line
                self.rules.add(line)
