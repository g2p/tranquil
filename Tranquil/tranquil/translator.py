
from django.conf import settings

from sqlalchemy import Table
from sqlalchemy.orm import mapper

def stringify(table):
	ret = ''
	for tok in table.split( '_' ):
		ret += tok.capitalize()
	return ret

def translate( meta, models ):
	sa_tables = {}
	sa_objects = {}
	for tbl in meta.table_iterator():
		if str( tbl ) in models:
			app = models[str(tbl)]._meta.app_label
			obj = models[str(tbl)]._meta.object_name
		else:
			app = getattr( settings, 'NO_MODEL_MODULE', 'dyn' )
			obj = stringify( str( tbl ) )
		if sa_objects.get( app ) is None:
			sa_objects[app] = []
		sa_tables[str(tbl)] = tbl
		ntype = type('%s' % obj, ( object, ), {} )
		sa_objects[app].append( ntype )
		mapper(ntype,tbl)
	return ( sa_tables, sa_objects )
