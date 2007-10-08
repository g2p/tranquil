
import datetime
import os
import sys
import unittest

sys.path.insert( 0, os.path.dirname( __file__ ) + '../' )
os.environ['DJANGO_SETTINGS_MODULE'] = 'proj_name.settings'
from django.conf import settings
setattr( settings, 'TRANQ_USE_DJANGO_MODELS', True )

from tranquil import Session
from tranquil.models.app_name import Poll

class DjangoModelTest(unittest.TestCase):
	def use_django_models_test(self):
		self.assertEqual( hasattr( Poll, '_sa_attribute_manager' ), True )
		self.assertEqual( hasattr( Poll, '_meta' ), True )
