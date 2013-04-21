# -*- Mode: Python; test-case-name: dirvune.test.test_vault -*-
# vi:si:et:sw=4:sts=4:ts=4

import os

import unittest

from dirvune import vault



class VaultTestCase(unittest.TestCase):

    def testVault(self):
        v = vault.Vault(os.path.join(os.path.dirname(__file__), 'vault'))

        images = v.getImages()
        self.assertEquals(len(images), 40)
        self.assertEquals(images[0], '20111011030000')


