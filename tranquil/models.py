
import new
import sys

from django.conf import settings
from django.db.models import signals
from django.db.models.loading import get_apps, get_models
from django.dispatch import dispatcher
from django.utils.encoding import force_unicode

from tranquil.translator import Translator, DEFAULT_NO_MODEL

__all__ = ( '__path__', 'Importer' )
__path__ = 'tranquil.models'

class Importer(object):
	def __init__(self,meta):
		self.meta = meta
		sys.meta_path.append( self )
		self.apps = set()
		self.cache = {}
		self.trans = None
		self.no_model = getattr( settings, 'TRANQ_NO_MODEL_MODULE', DEFAULT_NO_MODEL )
		dispatcher.connect(self.cache_model,signal=signals.class_prepared)

	def find_module(self,fullname,path=None):
		if len( self.apps ) == 0:
			get_models()
		if not self.no_model in self.apps:
			self.apps.add( self.no_model )
		if fullname.startswith('tranquil.models.'):
			app = fullname.replace( 'tranquil.models.', '' )
			if app in self.apps:
				return self
		return None
	
	def load_module(self,fullname):
		if self.trans is None:
			self.trans = Translator( self.meta, self.cache )
		if sys.modules.get( fullname ):
			return sys.modules[fullname]
		mod = sys.modules[fullname] = new.module(fullname)
		mod.__file__ = 'tranquil: %s' % fullname
		mod.__loader__ = self
		app = fullname.replace( 'tranquil.models.', '' )
		if self.trans.categorized.get( app ) is not None:
			for obj in self.trans.categorized[app]:
				setattr( mod, obj.__name__, obj )
		return mod

	def cache_model(self,sender=None):
		app = sender._meta.app_label
		if app not in self.apps:
			self.apps.add( app )
		table = sender._meta.db_table
		self.cache[table] = sender
	
