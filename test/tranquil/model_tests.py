
import cStringIO
import datetime
import os
import sys
import unittest

sys.path.insert( 0, '/usr/local/src/tranquil/' )
os.environ['DJANGO_SETTINGS_MODULE'] = 'proj_name.settings'

from django.core.management import execute_manager

sys.argv[1] = 'validate'
class ModelTest(unittest.TestCase):
	def test(self):
		import proj_name.settings
		execute_manager(proj_name.settings)
		from tranquil import Session
		from tranquil.models.app_name import Poll, Choice
		sa = Session()
		green = Poll()
		green.question = 'Do you like green eggs and ham?'
		green.pub_date = datetime.datetime.today()
		yes = Choice()
		yes.choice = 'Yes'
		yes.votes = 0
		no = Choice()
		no.choice = 'No'
		no.votes = 0
		green.choice_set.append(yes)
		green.choice_set.append(no)
		sa.save( green )
		sa.commit()
		sa = Session()
		p = sa.query(Poll).filter_by(id=1).one()
		self.assertEqual( len( p.choice_set ), 2 )
