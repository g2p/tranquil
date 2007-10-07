
import datetime
import os
import sys
import unittest

sys.path.insert( 0, os.path.dirname( __file__ ) + '../' )
os.environ['DJANGO_SETTINGS_MODULE'] = 'proj_name.settings'

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
			sess.delete(c)
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
		polls = sess.query(Poll).all()
		self.assertEqual( len( polls ), 1 )
		self.assertEqual( polls[0].question, 'Do you like green eggs and ham?' )
		self.assertEqual( len( polls[0].choice_set ), 2 )
		self.assertEqual( polls[0].choice_set[0].choice in ['Yes', 'No'], True )
		self.assertEqual( polls[0].choice_set[1].choice in ['Yes', 'No'], True )
