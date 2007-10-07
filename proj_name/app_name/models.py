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
	other = models.ForeignKey(Poll,related_name='other_set')
	tags = models.ManyToManyField(Tag)
	test = models.OneToOneField( Tag, related_name='test_set' )
	choice = models.CharField(max_length=200)
	votes = models.IntegerField()

	class Admin:
		pass
	
	def __unicode__(self):
		return "<Choice '%s'>" % self.choice
