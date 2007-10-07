#from ez_setup import use_setuptools
#use_setuptools()
from setuptools import setup, find_packages
from distutils.command.build_py import build_py as _build_py
from setuptools.command.sdist import sdist as _sdist
import re
import os
from os import path

class build_py(_build_py):
    def run(self):
        init = path.join(self.build_lib, 'tranquil', '__init__.py')
        if path.exists(init):
            os.unlink(init)
        _build_py.run(self)
        self.byte_compile([init])

class sdist(_sdist):
    def make_release_tree (self, base_dir, files):
        _sdist.make_release_tree(self, base_dir, files)
        orig = path.join('lib', 'tranquil', '__init__.py')
        assert path.exists(orig)
        dest = path.join(base_dir, orig)
        if hasattr(os, 'link') and path.exists(dest):
            os.unlink(dest)
        self.copy_file(orig, dest)
        _stamp_version(dest)

def _get_version():
    from subprocess import Popen, PIPE, STDOUT
    cmd = Popen( ['svnversion','-n'], stdout=PIPE, stderr=STDOUT )
    ver = cmd.communicate()[0]
    p = re.compile(  r'(?P<from>\d+)(:(?P<to>\d+)(\w+)?)?' )
    dict = p.match( ver ).groupdict()
    if dict.get( 'to' ) is not None:
       return dict['to']
    else:
       return dict['from']

VERSION = _get_version()

setup(name = "Tranquil",
      cmdclass={'build_py': build_py, 'sdist': sdist},
      version = VERSION,
      description = "Integration SQLAlchemy into Django",
      author = "Paul Davis",
      author_email = "paul.joseph.davis@gmail.com",
      url = "http://code.google.com/p/tranquil/",
      packages = find_packages('lib'),
      package_dir = {'':'lib'},
      license = "New BSD License",
      long_description = '',
      )
