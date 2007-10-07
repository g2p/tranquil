
import cStringIO
import datetime
import os
import sys
import unittest

sys.path.insert( 0, '/usr/local/src/tranquil/' )
os.environ['DJANGO_SETTINGS_MODULE'] = 'proj_name.settings'

from django.core.management import execute_manager
import proj_name.settings
sys.argv = [ './manage.py', 'validate' ]
execute_manager(proj_name.settings)

from tranquil import Session
from tranquil.models.app_name import Poll, Choice
from tranquil.translator import ORMObject

class ModelTest(unittest.TestCase):
	def ORMObject_test(self):
		obj = ORMObject(name='test')
		self.assertEqual( obj.name, 'test' )

	def clear(self):
		sess = Session()
		for c in sess.query(Choice):
			print dir( c )
			sess.delete(c)
		sess.commit()
		for p in sess.query(Poll):
			sess.delete(p)
		sess.commit()

	def model_test(self):
		self.clear()
		sess = Session()
		green = Poll(question='Do you like green eggs and ham?',pub_date=datetime.datetime.today())
		green.choice_set.append( Choice( choice='Yes', votes=0 ) )
		green.choice_set.append( Choice( choice='No', votes=0 ) )
		sess.save( green )
		sess.commit()
		sess = Session()
		polls = sess.query(Poll)
		self.assertEqual( len( polls ), 1 )
		self.assertEqual( len( polls[0].choice_set ), 2 )
