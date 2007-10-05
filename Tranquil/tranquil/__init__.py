
import re
#from django.core.exceptions import ImproperlyConfigured
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from tranquil.models import Importer

__all__ = ( 'engine', 'meta', 'Session', )

class EngineCache(object):
	__shared_state = dict(
		engine = None,
		meta = None,
		Session = None,
	)
	
	_mappings = {
		'sqlite3': 'sqlite',
		'mysql': 'mysql',
		'postgresql': 'postgres',
		'postgresql_psycopg2': 'postgres',
		'oracle': 'oracle',
	}
	
	def __init__(self):
		from django.conf import settings
		self.__dict__ = self.__shared_state
		if self.engine is None:
			options = {
				'protocol': self._mappings.get( settings.DATABASE_ENGINE ),
				'name': settings.DATABASE_NAME,
				'user': settings.DATABASE_USER,
				'pass': settings.DATABASE_PASSWORD,
				'host': settings.DATABASE_HOST,
				'port': settings.DATABASE_PORT,
			}
			if options['protocol'] is None:
				raise ImproperlyConfigured( 'Unknown database engine: %s' % settings.DATABASE_ENGINE )
			url = '{protocol}://{user}:{pass}@{host}{port}/{name}'
			for p in options:
				if p == 'port' and len( options[p] ) > 0:
					url = re.sub( '{%s}' % p, ':%s' % options[p], url )
				else:
					url = re.sub( '{%s}' % p, options[p], url )
			self.engine = create_engine( url )
			self.meta = MetaData(bind=self.engine,reflect=True)
			self.Session = sessionmaker( bind=self.engine, autoflush=True, transactional=True )
			self.importer = Importer(self.meta)

cache = EngineCache()
engine = cache.engine
meta = cache.meta
Session = cache.Session
