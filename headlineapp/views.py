import json
import calendar
from django.http import HttpResponse, HttpResponseRedirect, \
    HttpResponseNotModified, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from gripcontrol import HttpResponseFormat, HttpStreamFormat, \
    WebSocketMessageFormat
from django_grip import set_hold_longpoll, set_hold_stream, publish
from headlineapp.models import Headline

def _json_response(data):
    body = json.dumps(data, indent=4) + '\n' # pretty print
    return HttpResponse(body, content_type='application/json')

def base(request):
    if request.method == 'POST':
        h = Headline(type='none', title='', text='')
        h.save()
        return _json_response(h.to_data())
    else:
        return HttpResponseNotAllowed(['POST'])

def item(request, headline_id):
    h = get_object_or_404(Headline, pk=headline_id)

    hchannel = str(headline_id)

    if request.wscontext:
        ws = request.wscontext
        if ws.is_opening():
            ws.accept()
            ws.subscribe(hchannel)
        while ws.can_recv():
            message = ws.recv()
            if message is None:
                ws.close()
                break
        return HttpResponse()
    elif request.method == 'GET':
        if request.META.get('HTTP_ACCEPT') == 'text/event-stream':
            resp = HttpResponse(content_type='text/event-stream')
            set_hold_stream(request, hchannel)
            return resp
        else:
            wait = request.META.get('HTTP_WAIT')
            if wait:
                wait = int(wait)
                if wait < 1:
                    wait = None
                if wait > 300:
                    wait = 300
            inm = request.META.get('HTTP_IF_NONE_MATCH')
            etag = '"%s"' % calendar.timegm(h.date.utctimetuple())
            if inm == etag:
                resp = HttpResponseNotModified()
                if wait:
                    set_hold_longpoll(request, hchannel, timeout=wait)
            else:
                resp = _json_response(h.to_data())
            resp['ETag'] = etag
            return resp
    elif request.method == 'PUT':
        hdata = json.loads(request.read())

        h.type = hdata['type']
        h.title = hdata.get('title', '')
        h.text = hdata.get('text', '')
        h.save()
        hdata = h.to_data()

        hjson = json.dumps(hdata)
        etag = '"%s"' % calendar.timegm(h.date.utctimetuple())
        rheaders = {'Content-Type': 'application/json', 'ETag': etag}
        hpretty = json.dumps(hdata, indent=4) + '\n'

        formats = []
        formats.append(HttpResponseFormat(body=hpretty, headers=rheaders))
        formats.append(HttpStreamFormat('event: update\ndata: %s\n\n' % hjson))
        formats.append(WebSocketMessageFormat(hjson))

        publish(hchannel, formats)

        resp = _json_response(hdata)
        resp['ETag'] = etag
        return resp
    else:
        return HttpResponseNotAllowed(['GET', 'PUT'])
