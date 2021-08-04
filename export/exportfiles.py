#!/usr/bin/env python2

##########################################################################
#
#   Specialized verison of postfiles that will populate the filesystem
#   directories based on the current tincan stations.
#
#   2021-07-16  Todd Valentic
#               Initial implementation
#
##########################################################################

from postfiles import PostFiles

import os
import sys
import commands

class ExportFiles(PostFiles):

    def __init__(self, argv):
        PostFiles.__init__(self, argv)

        self.exportPath = self.get('path.project.export','.')

    def preprocess(self):

        stations = self.listStations()

        for station in stations:
            try:
                self.createFiles(station)
            except:
                self.log.exceptions('Failed to make dirs for %s' % station)

    def listStations(self):

        sql = 'select name from mesh_node where active=true'
        sqlcmd = 'psql -d tincan -t -c "%s"' % sql

        status, output = commands.getstatusoutput(sqlcmd)

        if status == 0:
            return output.split()
        else:
            self.log.error('Failed to get station list')
            self.log.error('cmd=%s' % sqlcmd)
            self.log.error('output=%s' % output)
            return []

    def createFiles(self, station): 

        basepath = os.path.join(self.exportPath, station)

        for filegroup in self.filegroups:
            path = os.path.join(basepath, filegroup.name)

            if not os.path.exists(path):
                try:
                    original_umask = os.umask(0)
                    os.makedirs(path, mode=0o775)
                    self.log.info('Creating %s' % path)
                except:
                    self.log.exception('Failed to create %s' % path)
                finally:
                    os.umask(original_umask)
        
if __name__ == '__main__':
    ExportFiles(sys.argv).run()


