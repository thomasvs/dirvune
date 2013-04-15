# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

import subprocess
import commands

def parsedate(description, now):
    output = commands.getoutput(
"""perl -e 'use Time::ParseDate; print parsedate("%s", NOW => %d);'""" % (
                description, now))
    return int(output)

def inPeriod(time, period):
    output = commands.getoutput(
"""perl -e 'use Time::Period; print inPeriod("%d", "%s");'""" % (
                time, period))
    return int(output)


class Perl(object):

    def __init__(self):
        pass

    def start(self):
        # $| = 1 sets autoflush on; see perlvar; this way we can
        # interact line by line
        self._pipe = subprocess.Popen(["perl", "-n", "-e",
            '$| = 1; eval($_); print "\\n";'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)

    def stop(self):
        self._pipe.stdin.close()

    def inPeriod(self, time, period):
        command = 'use Time::Period; print inPeriod(%d, "%s");\n' % (
            time, period)
        self._pipe.stdin.write(command)
        output = self._pipe.stdout.readline()
        return int(output)


