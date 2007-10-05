
__all__ = ( '__path__', 'Importer' )
__path__ = 'tranquil.models'

import new
import sys

from django.conf import settings
from django.db.models import signals
from django.db.models.loading import get_models
from django.dispatch import dispatcher
from django.utils.encoding import force_unicode

from tranquil.translator import translate

class Importer(object):
	def __init__(self,meta):
		self.meta = meta
		sys.meta_path.append( self )
		self.apps = set()
		self.apps.add( getattr( settings, 'NO_MODEL_MODULE', 'dyn' ) )
		self.cache = {}
		self.tables = None
		self.objects = None
		dispatcher.connect(self.cache_model,signal=signals.class_prepared)
		#for model in get_models():
		#	self.cache_model(sender=model)

	def find_module(self,fullname,path=None):
		if fullname.startswith('tranquil.models.'):
			app = fullname.replace( 'tranquil.models.', '' )
			if app in self.apps:
				return self
		return None
	
	def load_module(self,fullname):
		print 'MODULE: %s' % fullname
		if self.tables is None:
			( self.tables, self.objects ) = translate( self.meta, self.cache )
		if sys.modules.get( fullname ):
			return sys.modules[fullname]
		print 'LOADING: %s' % fullname
		mod = sys.modules[fullname] = new.module(fullname)
		mod.__file__ = 'tranquil: %s' % fullname
		mod.__loader__ = self
		app = fullname.replace( 'tranquil.models.', '' )
		print self.objects.get( app, 'Not here!' )
		if self.objects.get( app ) is not None:
			for obj in self.objects[app]:
				print 'APP: %s TYPE: %s' % ( app, obj.__name__ )
				setattr( mod, obj.__name__, obj )
		return mod

	def cache_model(self,sender=None):
		app = sender._meta.app_label
		if app not in self.apps:
			self.apps.add( app )
		table = sender._meta.db_table
		print 'APP: %s TABLE: %s' % ( app, table )
		self.cache[table] = sender	
	
