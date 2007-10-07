
from distutils.core import setup

def _read(file):
	curr = open( file, 'r' )
	data = ''.join( [ l for l in  curr ] )
	curr.close()
	return data

def _write(file,VERSION):
	curr = open( file, 'w' )
	curr.write( '%s\n', VERSION )
	curr.close()

def _parse(data):
	import re
	pattern = re.compile( r'(?P<from>\d+)(:(?P<to>\d+)(\w+)?)?' )
	dict = pattern.match( data ).groupdict()
	if dict.get( 'to' ) is not None:
		return dict['to']
	elif dict.get( 'from' ) is not None:
		return dict['from']
	else:
		return None

def _get_version():
	import os
	path = os.path.join( os.path.dirname( __file__ ), 'VERSION' )
	curr = _parse( _read( path ).strip() )
	os.system( 'svnversion > %s' % path )
	next = _parse( _read( path ).strip() )
	if curr is None and next is None:
		return 'alpha'
	elif curr is not None and next is None:
		return curr
	elif curr is None and next is not None:
		return next
	elif int( curr ) > int( next ):
		return curr
	else:
		_write(path,next)
		return next

VERSION=_get_version()
print "VERSION: %s" % VERSION

PACKAGES=[
	'tranquil',
	'tranquil.middleware',
]

PACKAGE_DATA={}

setup(	name="Tranquil",
		version=VERSION,
		description="Integrating SQLAlchemy with Django",
		long_description="",
		author="Paul Davis",
		author_email="paul.joseph.davis@gmail.com",
		url="http://code.google.com/p/tranquil/",
		packages=PACKAGES,
		package_data=PACKAGE_DATA,
)
