from tranquil import Session

class SqlAlchemySession(object):
	def process_request(self, request):
		request.sa = Session()
	
	def process_exception(self, request, exception):
		sess = getattr( request, 'sa', None )
		if sess is not None:
			sess.close()

	def process_response(self, request, response):
		sess = getattr( request, 'sa', None )
		if sess is not None:
			sess.close()
		return response
