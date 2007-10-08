
from inspect import getmembers

from django.conf import settings
from django.db.models.related import RelatedObject
from django.db.models.fields.related import RelatedField

from sqlalchemy import Table
from sqlalchemy.orm import backref, compile_mappers, mapper, relation
from sqlalchemy.orm.mapper import Mapper

DEFAULT_NO_MODEL='dyn'

def load_custom(meta,tables):
	mappers = {}
	for app in settings.INSTALLED_APPS:
		mod = __import__( app, {}, {}, [ 'alchemy', ] )
		if not hasattr( mod, 'alchemy' ):
			continue
		for obj in mod.alchemy.__dict__:
			attr = getattr( mod.alchemy, obj )
			if isinstance( attr, Table ):
				meta.remove( tables[ str( attr ) ] )
				tables[str( attr )] = attr.tometadata(meta)
			elif isinstance( attr, Mapper ):
				mappers[attr.local_table] = attr
	return ( tables, mappers )

class ORMObject(object):
	def __init__(self,**kwargs):
		for arg in kwargs:
			setattr(self,arg,kwargs[arg])

class Relation(object):
	def __init__(self,model,field):
		self.model = model
		self.field = field
	
	def get_backref(self):
		if self.field.rel.multiple:
			if getattr( self.field.rel, 'symmetrical', False ) and self.model == self.field.rel.to:
				return None
			return self.field.rel.related_name or ( self.model._meta.object_name.lower() + '_set' )
		else:
			return self.field.rel.related_name or ( self.model._meta.object_name.lower() )
	
	def get_m2m_table(self):
		if self.field.rel.multiple:
			return self.field._get_m2m_db_table( self.model._meta )
		return None
	
	def add_fkey(self,kwargs,column):
		if kwargs.get( 'foreign_keys' ) is None:
			kwargs['foreign_keys'] = []
		kwargs['foreign_keys'].append( column )
		return kwargs
	
	def props(self,tables,mt_map):
		kwargs = {}
		fn = getattr( self, self.field.__class__.__name__ )
		kwargs = fn( kwargs, tables, mt_map )
		brefargs = kwargs.copy()
		if brefargs.get( 'secondary' ) is not None:
			del brefargs['secondary']
		kwargs['backref'] = backref( self.get_backref(), **brefargs )
		return kwargs
	
	def add_primary_join(self,kwargs,mt_map):
		fr = mt_map[self.model]
		to = mt_map[self.field.rel.to]
		fcol = getattr( fr.c, self.field.get_attname() )
		tcol = getattr( to.c, self.field.rel.field_name )
		kwargs['primaryjoin'] = fcol==tcol
		kwargs = self.add_fkey( kwargs, fcol )
		return kwargs
	
	def ForeignKey(self,kwargs,tables,mt_map):
		return self.add_primary_join( kwargs, mt_map )

	def OneToOneField(self,kwargs, tables, mt_map):
		kwargs['uselist'] = False
		return self.add_primary_join( kwargs, mt_map )
	
	def ManyToManyField(self,kwargs,tables,mt_map):
		related = RelatedObject( self.field.rel.to, self.model, self.field )
		kwargs['secondary'] = tables[ self.field._get_m2m_db_table( self.model._meta ) ]
		fr = mt_map[self.model]
		to = tables[self.get_m2m_table()]
		fcol = getattr( fr.c, self.model._meta.pk.get_attname() )
		tcol = getattr( to.c, self.field._get_m2m_column_name( related ) )
		kwargs['primaryjoin'] = fcol==tcol
		kwargs = self.add_fkey( kwargs, tcol )
		fr = to
		to = mt_map[self.field.rel.to]
		fcol = getattr( fr.c, self.field._get_m2m_reverse_name( related ) )
		tcol = getattr( to.c, self.field.rel.to._meta.pk.get_attname() )
		kwargs['secondaryjoin'] = fcol==tcol
		kwargs = self.add_fkey( kwargs, fcol )
		return kwargs

class Translator(object):
	def __init__( self, meta, models ):
		self.meta = meta
		self.models = models
		self.tables = {}
		self.objects = {}
		self.categorized = {}
		self.mt_map = {}
		self.mo_map = {}
		self.use_django_models = getattr( settings, 'TRANQ_USE_DJANGO_MODELS', False )
		for table in meta.table_iterator():
			self.tables[ str(table) ] = table
		( self.tables, self.mappers ) = load_custom( self.meta, self.tables )
		self.relations = self.backreferences()
		for tname in self.tables:
			table = self.tables[tname]
			if tname in models:
				model = models[tname]
				app = model._meta.app_label
				obj = model._meta.object_name
			else:
				model = None
				app = getattr( settings, 'TRANQ_NO_MODEL_MODULE', DEFAULT_NO_MODEL )
				obj = self.stringify( tname )
			if self.categorized.get( app ) is None:
				self.categorized[app] = []
			if self.use_django_models and model and model is not None:
				self.objects[tname] = model
			else:
				self.objects[tname] = type( obj, ( ORMObject, ), {} )
			self.categorized[app].append( self.objects[tname] )
			if model is not None:
				self.mt_map[model] = table
				self.mo_map[model] = self.objects[tname]
		self.map()

	def stringify(self,table):
		ret = ''
		for tok in table.split( '_' ):
			ret += tok.capitalize()
		return ret

	def backreferences(self):
		rels = {}
		for name in self.models:
			model = self.models[name]
			for field in model._meta.fields + model._meta.many_to_many:
				if field.rel:
					if rels.get( model ) is None:
						rels[model] = []
					rels[model].append( Relation( model, field ) )
		return rels
	
	def map(self):
		for table in self.tables:
			if table in self.mappers:
				continue
			props = {}
			if table in self.models and self.models[table] in self.relations:
				model = self.models[table]
				props = {}
				for rel in self.relations[model]:
					props[rel.field.name] = relation( self.mo_map[rel.field.rel.to],
														**rel.props( self.tables, self.mt_map ) )
			if len( props ) > 0:
				mapper(self.objects[table],self.tables[table],properties=props)
			else:
				mapper(self.objects[table],self.tables[table])
		compile_mappers()
