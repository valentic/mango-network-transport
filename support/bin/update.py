#!/usr/bin/env python2

#########################################################
#
#   Update tables
#
#   2012-11-09  Todd Valentic
#               Initial implementation
#
#########################################################

import sys
import optparse
import mixinconfig
import logging

import model

logging.basicConfig(level=logging.INFO)

class Reload:

    def __init__(self,configfile,options):

        config = mixinconfig.MixinConfigParser()
        config.read(configfile)

        self.options = options

        current = {}

        for section in config.sections():

            _class = getattr(model,config.get(section,'_class'))

            if _class in current:
                current[_class].append(section)
            else:
                current[_class] = [section]

            params = {}

            for key in config.options(section):
                if not key.startswith('_'):
                    params[key] = config.get(section,key)

            # filter to match columns in database

            attrs = _class.__dict__.keys()
            params = dict((k,v) for k,v in params.items() if k in attrs)

            match = {}
            for key in config.getList(section,'_match'):
                match[key]=params[key]

            instance = _class.query.filter_by(**match).first()

            if instance:
                logging.info('Updating %s',section)
                for k,v in params.iteritems():
                    setattr(instance,k,v)

            else:

                instance = _class(**params)
                model.add(instance)

                logging.info('Adding %s' % section)

        #self.expire(current)

        try:
            model.commit()
            logging.info('Commiting')
        except:
            model.rollback()
            logging.exception('Failed to commit')
            sys.exit(1)

    def expire(self,current):

        for _class,curnames in current.items():
            oldobjs = dict([(str(k.id),k) for k in _class.query.all()])
            expired = set(oldobjs).difference(curnames)
            for name in expired:
                obj = oldobjs[name]
                model.delete(obj)
                logging.info('Expired %s' % obj)

if __name__ == '__main__':

    usage = '%prog config'

    parser = optparse.OptionParser(usage=usage)

    options,args = parser.parse_args()

    if len(args)<1:
        parser.error('Need to specify config file')

    for filename in args:
        Reload(filename,options)

    sys.exit(0)


