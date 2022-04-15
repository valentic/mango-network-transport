#!/usr/bin/env python

########################################################################
#
#   Store records into database.
#
#   Handles a generic class of data records. Match based on newsgroup
#   name.
#
#   2021-09-14  Todd Valentic
#               Initial implementation. Adapted for mango
#
########################################################################

from Transport  import ProcessClient
from Transport  import NewsPollMixin
from Transport  import NewsTool

import os
import sys
import fnmatch

import model
import artemis_store

DataProcessor = {
    'greenline':        artemis_store.Store(),
    'redline':          artemis_store.Store(),
    }

DataFiles = {
    'greenline':        ['*.dat.bz2'],
    'redline':          ['*.dat.bz2'],
    }

class StoreDB(ProcessClient,NewsPollMixin):

    def __init__(self,args):
        ProcessClient.__init__(self,args)
        NewsPollMixin.__init__(self,callback=self.process)

    def process(self,message):

        # newsgroup: transport.mango.station.<sitename>.outbound.<instrument>
        #                0       1      2         3         4         5
        # i.e. transport.mango.station.lwl.outbound.greenline

        newsgroup = message['Newsgroups'].split('.')
        servername = message['Xref'].split()[0]
        datatype  = newsgroup[-1]
        location  = newsgroup[1]
        sitename  = newsgroup[3]
        store     = DataProcessor[datatype]
        timestamp = NewsTool.messageDate(message)

        self.log.info('%s - %s - %s' % (sitename,datatype,timestamp))

        opts = dict(
                servername=servername,
                datatype=datatype,
                location=location,
                sitename=sitename,
                timestamp=timestamp)

        for filename in NewsTool.saveFiles(message):
            if self.matchFilename(filename,DataFiles[datatype]):
                store.process(filename,opts=opts)
            os.remove(filename)

    def matchFilename(self,filename,patterns):

        for pattern in patterns:
            if fnmatch.fnmatch(filename,pattern):
                return True

        return False

if __name__ == '__main__':
    StoreDB(sys.argv).run()

