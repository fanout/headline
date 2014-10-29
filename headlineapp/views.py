import json
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from gripcontrol import HttpResponseFormat, HttpStreamFormat, WebSocketMessageFormat
from django_grip import set_hold_longpoll, set_hold_stream, publish
from headlineapp.models import Headline

def base(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        title = request.POST.get('title', '')
        text = request.POST.get('text')
        h = Headline(type=type, title=title, text=text)
        h.save()
        return HttpResponse(json.dumps(h.to_data(), indent=4))
    else:
        return HttpResponseNotAllowed(['POST'])

def item(request, headline_id):
    h = get_object_or_404(Headline, pk=headline_id)
    if request.wscontext:
        ws = request.wscontext
        if ws.is_opening():
            ws.accept()
            ws.subscribe('headline-%s' % headline_id)
        while ws.can_recv():
            message = ws.recv()
            if message is None:
                ws.close()
                break
    elif request.method == 'GET':
        return HttpResponse(json.dumps(h.to_data(), indent=4))
    elif request.method == 'PUT':
        h.type = request.POST.get('type')
        h.title = request.POST.get('title', '')
        h.text = request.POST.get('text')
        h.save()
        formats = list()
        formats.append(WebSocketMessageFormat(json.dumps(h.to_data())))
        publish('headline-%s' % headline_id, formats)
        return HttpResponse(json.dumps(h.to_data(), indent=4))
