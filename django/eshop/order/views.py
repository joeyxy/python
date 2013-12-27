from django.http import Http404,HttpResponse
import datetime
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from order.models import Book

def search_form(request):
	return render_to_response('search_form.html')

def search(request):
	error = False
	if 'q' in request.GET:
		q = request.GET['q']
		if not q:
			error = True
			return render_to_response('search_form.html',{'error':error})
		else:
			books = Book.objects.filter(title__icontains=q)
			return render_to_response('search_results.html',{'books':books,'query':q})
		#message = 'You searched for: %r' % request.GET['q']
	else:
		#message = 'You submitted an empty form.'
		#return HttpResponse(message)
		return render_to_response('search_form.html',{'error':error})
def ua_display(request):
	ua = request.META.get('HTTP_USER_AGENT','unknown')
	return HttpResponse("Your browser is %s" % ua)

def display_meta(request):
	values = request.META.items()
	values.sort()
	html = []
	for k,v in values:
		html.append('<tr><td>%s</td><td>%s</td></tr>'%(k,v))
	return HttpResponse('<table border=1>%s</table>' % '\n'.join(html))


def hello(request):
	return HttpResponse("Hello world")

def current_url(request):
	return HttpResponse("Welcome to the page at %s" % request.path)

def current_datetime(request):
	now = datetime.datetime.now()
        #1.
	#html = "<html><body>It is now %s.</body></html>" % now
	#2.
	#t = get_template('current_datetime.html')
	#html = t.render(Context({'current_date':now}))
	#return HttpResponse(html)
	return render_to_response('current_datetime.html',{'current_date':now})

def hours_ahead(request,offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	dt = datetime.datetime.now()+ datetime.timedelta(hours=offset)
	html = "<html><body>In %s hour(s),it will be %s.</body></html>" % (offset,dt)
	return HttpResponse(html)
