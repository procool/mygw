import os, sys, stat, imp
import logging


class Extention(object):
    def __init__(self, mod, filename, name, enabled=True):
        self.filename = filename
        self.name = name
        self.mod = mod
        self.enabled = enabled

    def __call__(self):
        return self.mod
       
    

class Plugins(object):

    extensions = []

    @staticmethod
    def get_plugins_path(dirname):
        for path in sys.path:
            p = "/".join((path, dirname))
            if os.path.exists(p):
                return p


    @classmethod
    def register_plugin(cls, name, fpath, is_file):
        dirpath = os.path.dirname(fpath)
        filename, file_extension = os.path.splitext(name)
        if not file_extension in ('.py', '.pyc', ''):
            raise Exception("not a python file")
        if file_extension == '' and is_file:
            raise Exception("not a python module")
        fp, pathname, description = imp.find_module(filename, [dirpath,])
        try:
            mod_ = imp.load_module(filename, fp, pathname, description)
        finally:
            if fp:
                fp.close()
        cls.find_extentions(mod_, name=filename)
        return True


    @classmethod
    def find_extentions(cls, mod_, name=None):
        for extname in dir(mod_):
            extension = getattr(mod_, extname)
            if not hasattr(extension, 'enabled'):
                continue
            if not extension.enabled:
                continue
            cls.add_extension(extension, name, extname)


    @classmethod
    def add_extension(cls, extension, name=None, extname=None):
        logging.info("PLUGIN: Loading extention: %s/%s" % (name, extname))
        cls.extensions.append(Extention(extension, name, extname))

    @classmethod
    def get_enabled_extensions(cls):
        for ext_ in cls.extensions:
            if not ext_.enabled:
                continue
            yield ext_


    @classmethod
    def init(cls, dirpath='plugins'):
        loaded_files = []
        path_ = cls.get_plugins_path(dirpath)
        sys.path.append(path_)
        if path_ is None:
            logging.error('Can not find plugins in directory: %s' % dirpath)
            return None
        for name in os.listdir(path_):
            fpath = os.path.abspath("/".join((path_, name)))
            fstat = os.stat(fpath)

            is_file = True
            if not stat.S_ISREG(fstat.st_mode):
                is_file = False

            filename, file_extension = os.path.splitext(fpath)
            if filename in loaded_files:
                continue
            try: 
                cls.register_plugin(name, fpath, is_file)
                loaded_files.append(filename)
            except Exception as err: 
                logging.error('Error on loading plugin: %s: %s' % (name, err))


if __name__ == '__main__':
    Plugins.init('plugins') 
    print Plugins.extensions


