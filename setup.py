
from distutils.core import setup

PACKAGES=[
	'tranquil',
	'tranquil.middleware',
]

PACKAGE_DATA={}

setup(	name="Tranquil",
		version="11",
		description="Integrating SQLAlchemy with Django",
		long_description="",
		author="Paul Davis",
		author_email="paul.joseph.davis@gmail.com",
		url="http://code.google.com/p/tranquil/",
		packages=PACKAGES,
		package_data=PACKAGE_DATA,
)
