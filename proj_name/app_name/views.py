# Create your views here.

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from tranquil.models.app_name import Poll, Choice

def index(request):
	polls = request.sa.query(Poll)
	return render_to_response( 'polls/index.html', { 'polls': polls } )

def detail(request,poll_id):
	poll = request.sa.query(Poll).filter(Poll.id==poll_id).one()
	choices = request.sa.query(Choice).filter_by( poll_id=poll_id )
	return render_to_response( 'polls/detail.html', { 'poll': poll, 'choices': choices } )

def results(request,poll_id):
	poll = request.sa.query(Poll).filter(Poll.id==poll_id).one()
	choices = request.sa.query(Choice).filter_by( poll_id=poll_id )
	return render_to_response( 'polls/results.html', { 'poll': poll, 'choices': choices } )

def vote(request,poll_id,choice_id):
	choice = request.sa.query(Choice).filter_by(poll_id=poll_id).filter_by(id=choice_id).one() 
	choice.votes += 1
	request.sa.save(choice)
	request.sa.commit()
	return HttpResponseRedirect( reverse( 'results', args=(poll_id, ) ) )
	
