# -*- Mode: Python; test-case-name: dirvune.test.test_vault -*-
# vi:si:et:sw=4:sts=4:ts=4

import os
import glob


class Vault:
    """
    I represent a vault in dirvish.
    """
    def __init__(self, path):
        self._path = path
        if not os.path.isdir(path):
            raise KeyError("%s is not a directory" % path)

    def getImages(self):
        """
        Return a list of successful images, ordered.
        """
        ret = []

        candidates = os.listdir(self._path)
        for c in candidates:
            if c == 'dirvish':
                continue

            path = os.path.join(self._path, c)
            if not os.path.isdir(path):
                continue

            s = os.stat(path)
            # dirvish locks out anyone but owner if it failed
            if s.st_mode == 040700:
                continue

            # rsync errors can happen for good backups too
            # if glob.glob('%s/rsync_error*' % path):
            #     print 'rsync error, skipping', path
            #     continue

            ret.append(c)

        ret.sort()

        return ret
