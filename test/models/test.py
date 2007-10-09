
import datetime
import os
import sys
import unittest

sys.path.insert( 0, os.path.dirname( __file__ ) + '../' )
os.environ['DJANGO_SETTINGS_MODULE'] = 'proj_name.settings'

from tranquil import Session
from tranquil.models.app_name import Poll, Choice, SelfRef, MultiSelfRef
from tranquil.translator import ORMObject

from proj_name.app_name.alchemy import User

class ModelTest(unittest.TestCase):
	def ORMObject_test(self):
		obj = ORMObject(name='test')
		self.assertEqual( obj.name, 'test' )

	def clear(self,klass):
		sess = Session()
		for k in sess.query(klass).all():
			sess.delete(k)
		sess.commit()

	def model_test(self):
		self.clear(Choice)
		self.clear(Poll)
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
		self.assert_( polls[0].choice_set[0].choice in ['Yes', 'No'] )
		self.assert_( polls[0].choice_set[1].choice in ['Yes', 'No'] )
	
	def custom_test(self):
		sess = Session()
		me = sess.query(User).filter_by(username='davisp').one()
		self.assertEqual( me.name(), 'username=davisp' )

	def self_ref_test(self):
		self.clear(SelfRef)
		sess = Session()
		root = SelfRef(name='root')
		sess.save( root )
		c1 = SelfRef(name='c1',parent=root)
		sess.save( c1 )
		sess.commit()
		sess = Session()
		root = sess.query(SelfRef).filter(SelfRef.c.id==1).one()
		self.assertEqual( root.name, 'root' )
		self.assertEqual( len( root.selfref_set ), 1 )
		self.assertEqual( root.parent, None )
		child = root.selfref_set[0]
		self.assertEqual( child.name, 'c1' )
		self.assertEqual( child.parent, root )
		self.assertEqual( child.selfref_set, [] )
	
	def multi_self_ref_test(self):
		self.clear(MultiSelfRef)
		sess = Session()
		root = MultiSelfRef(name='root')
		root.ref.append( MultiSelfRef(name='c1') )
		root.ref.append( MultiSelfRef(name='c2') )
		root.multiselfref_set.append( MultiSelfRef(name='p1') )
		sess.save( root )
		sess.flush()
		sess = Session()
		n = sess.query(MultiSelfRef).filter(MultiSelfRef.c.name=='root').one()
		self.assertEqual( len( n.ref ), 2 )
		self.assert_( 'c1' in [ t.name for t in n.ref ] )
		self.assert_( 'c2' in [ t.name for t in n.ref ] )
		self.assertEqual( len( n.multiselfref_set ), 1 )
		self.assert_( 'p1' in [ t.name for t in n.multiselfref_set ] )
		for name in [ 'c1', 'c2']:
			n = sess.query(MultiSelfRef).filter(MultiSelfRef.c.name==name).one()
			self.assertEqual( n.ref, [] )
			self.assertEqual( len( n.multiselfref_set ), 1 )
			self.assert_( 'root' in [ t.name for t in n.multiselfref_set ] )
		n = sess.query(MultiSelfRef).filter(MultiSelfRef.c.name=='p1').one()
		self.assertEqual( len( n.ref ), 1 )
		self.assert_( 'root' in [ t.name for t in n.ref ] )
		self.assertEqual( n.multiselfref_set, [] )
