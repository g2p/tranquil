
from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData
from sqlalchemy.orm import mapper

meta = MetaData()

users = Table( 'auth_user', meta,
	Column('id',Integer,primary_key=True),
	Column('username',String(30)),
	Column('first_name',String(30)),
	Column('last_name',String(30)),
)

class User(object):
	def name(self):
		return "username=%s" % self.username

UserMapper = mapper(User,users)

