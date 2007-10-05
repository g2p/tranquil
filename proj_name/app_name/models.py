from django.db import models

class Poll(models.Model):
	question = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date_published')
	
	class Admin:
		pass
	
	def __unicode__(self):
		return "<Poll '%s'>" % self.question

class Choice(models.Model):
	poll = models.ForeignKey(Poll)
	choice = models.CharField(max_length=200)
	votes = models.IntegerField()

	class Admin:
		pass
	
	def __unicode__(self):
		return "<Choice '%s'>" % self.choice
