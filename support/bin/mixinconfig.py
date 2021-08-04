#!/usr/bin/env python

##########################################################################
#
#   Mixin enhanced ConfigParser
#
#   2012-04-26  Todd Valentic
#               Initial implementation
#
#   2014-02-14  Todd Valentic
#               Return non-mixin options in DEFAULTS in options()
#
##########################################################################

from ConfigParser import SafeConfigParser

class MixinConfigParser(SafeConfigParser):

    def options(self,section):

        opts = self._sections[section].keys()
        opts.remove('__name__')

        if 'mixin' in opts:
            opts.remove('mixin')

        mixins = self.mixins(section)

        for option in self._defaults:
            for mixin in mixins:
                if option.startswith(mixin):
                    key = option.replace(mixin+'.','')
                    if key not in opts:
                        opts.append(key)
                    continue
            opts.append(option)

        return opts


    def mixins(self,section):
        if self.has_option(section,'mixin'):
            return SafeConfigParser.get(self,section,'mixin').split()
        else:
            return []

    def get(self,section,option,default=None,**kw):

        lookupStack = [option]

        for mixin in self.mixins(section):
            lookupStack.append('%s.%s' % (mixin,option))

        for option in lookupStack:
            if self.has_option(section,option):
                return SafeConfigParser.get(self,section,option,**kw)

        return default

    def getint(self,section,option,default=None,**kw):
        try:
            return SafeConfigParser.getint(self,section,option,**kw)
        except:
            return default

    def getfloat(self,section,option,default=None,**kw):
        try:
            return SafeConfigParser.getfloat(self,section,option,**kw)
        except:
            return default

    def getboolean(self,section,option,default=None,**kw):
        try:
            return SafeConfigParser.getboolean(self,section,option,**kw)
        except:
            return default

    def getList(self,*pos,**kw):
        return self.get(*pos,**kw).split()

if __name__ == '__main__':

    config = MixinConfigParser()
    config.read('buoys.conf')

    print 'Looking up OB2.uuid'
    print '[OB2] uuid = %s' % config.get('OB2','uuid')

    print 'Looking up OB2.revision'
    print '[OB2] revision = %s' % config.getint('OB2','revision')

    print 'Looking up OB2.institution'
    print '[OB2] institition = %s' % config.get('OB2','institution')

    print 'Looking up OB2.name'
    print '[OB2] name = %s' % config.get('OB2','name')

    print 'Options for OB2'
    print config.options('OB2')

    for opt in config.options('OB2'):
        print opt,config.get('OB2',opt)


