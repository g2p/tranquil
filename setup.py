
from distutils.core import setup

def _read_version():
	import os
	file = os.path.join( os.path.dirname( __file__ ), 'VERSION' )
	curr = open( file, 'r' )
	data = ''.join( [ l for l in  curr ] ).strip()
	curr.close()
	return data

VERSION=_read_version()

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
