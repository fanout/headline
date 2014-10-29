from django.http import HttpResponse

def base(request):
	return HttpResponse('base')

def item(request, headline_id):
	return HttpResponse('item %s' % headline_id)
