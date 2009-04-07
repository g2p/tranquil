from django.db import models

class Poll(models.Model):
	question = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date_published')
	
	class Admin:
		pass
	
	def __unicode__(self):
		return "<Poll '%s'>" % self.question

class Tag(models.Model):
	name = models.CharField(max_length=200)

class Choice(models.Model):
	poll = models.ForeignKey(Poll)
	tags = models.ManyToManyField(Tag)
	choice = models.CharField(max_length=200)
	votes = models.IntegerField()

	class Admin:
		pass
	
	def __unicode__(self):
		return "<Choice '%s'>" % self.choice

class SelfRef(models.Model):
	parent = models.ForeignKey('self',null=True)
	name = models.CharField(max_length=50)

class MultiSelfRef(models.Model):
	name = models.CharField(max_length=50)
	ref = models.ManyToManyField('self')

class PositionedTag(Tag):
	position = models.IntegerField()

