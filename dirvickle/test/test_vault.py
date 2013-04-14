# -*- Mode: Python; test-case-name: dirvickle.test.test_vault -*-
# vi:si:et:sw=4:sts=4:ts=4

import os

import unittest

from dirvickle import vault



class VaultTestCase(unittest.TestCase):

    def testVault(self):
        v = vault.Vault(os.path.join(os.path.dirname(__file__), 'vault'))

        images = v.getImages()
        self.assertEquals(len(images), 38)
        self.assertEquals(images[0], '20120731030000')


