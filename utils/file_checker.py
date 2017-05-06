#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import os

class fileChecker():
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    def __init__(self, logger = None):
        self.logger = logger
    def exists(self, name):
        exists = os.path.exists(name)
        if not exists:
            if self.logger:
                self.logger.debug('exists: ' + str(exists) + ': '+ name)
        return exists
    def isEmpty(self, name):
        size = 1
        if self.exists(name):
            try:
                size = os.path.getsize(name)
            except OSError as e:
                if self.logger:
                    self.logger.error(e)
            if self.logger:
                self.logger.debug('size: ' + self.humansize(size))
        return not(size > 0)
    def process(self, name):
        return self.exists(name) and not self.isEmpty(name)

    def humansize(self, nbytes):
        if nbytes == 0: return '0 B'
        i = 0
        while nbytes >= 1024 and i < len(self.suffixes)-1:
            nbytes /= 1024.
            i += 1
        f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
        return '%s %s' % (f, self.suffixes[i])

# if __name__ == '__main__':
    # print __package__
    # print __name__
    # print __file__
