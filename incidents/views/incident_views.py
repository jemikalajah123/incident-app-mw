from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from ..models import Parcel, Incident
import json
import sys, traceback


# TODO: use a logging library
def getIncidents(request):
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)

            data = _read_from_file(filename)

            # if this incident number is already in the db,
            # ignore the file and retrieve what's in the db.
            # TODO: reconsider overwriting the current db record.
            try:
                if 'description' in data and 'incident_number' in data['description']:
                    incident = Incident.objects.get(incident_number=data['description']['incident_number'])
                    print('{} already in database.  Using database record.'.format(incident))
                    parcel = incident.incident_parcel
                else:
                    raise Exception('no incident number found.  Check File.')
            except Exception as e:
                # We keep going
                parcel = Parcel()
                enricher = Enricher(data)
                enricher.enrich(parcel)
                parcel.save()
                # print(parcel)

                incident = _create_incident(data, parcel)
                enricher.enrich(incident)
                incident.save()
                # print(incident)

            return render(request, 'cad/index.html', {
                'uploaded_file_url': uploaded_file_url,
                'incident': incident,
                'marker': {
                    'lat': incident.incident_latitude,
                    'lng': incident.incident_longitude
                },
                'weather': incident.incident_weather_description,
                'parcel_poly': parcel.get_polygon(),
                'parcel': parcel,
                'response_unit_stats': incident.get_response_unit_stats()
            })
        else:
            template = loader.get_template('cad/index.html')
            context = {}
            return HttpResponse(template.render(context, request))
    except Exception as e:
        # Exception catch-all.  Mostly to let user know about parse errors.
        traceback.print_exc(file=sys.stdout)
        return render(request, 'cad/index.html', {
            'error_msg': str(e)
        })


def _create_incident(data, parcel):
    inc = Incident(incident_parcel=parcel)
    if 'description' in data and 'incident_number' in data['description']:
        inc.incident_number = data['description']['incident_number']
    else:
        raise Exception('Cannot find incident_number.  Check File')

    if 'address' in data and \
            'latitude' in data['address'] and \
            'longitude' in data['address']:
        inc.incident_latitude = data['address']['latitude']
        inc.incident_longitude = data['address']['longitude']
    else:
        raise Exception('lat/long not found in address. Check file')

    if 'address' in data and \
            'address_line1' in data['address'] and \
            'city' in data['address'] and \
            'state' in data['address']:
        a = data['address']
        inc.incident_address_string = '{} {}, {}'.format(a['address_line1'], a['city'], a['state'])

    if 'address' in data and \
            'response_zone' in data['address']:
        inc.incident_response_zone = data['address']['response_zone']

    if 'description' in data:
        if 'type' in data['description']:
            inc.incident_type = data['description']['type']
        if 'subtype' in data['description']:
            inc.incident_sub_type = data['description']['subtype']
        if 'day_of_week' in data['description']:
            inc.incident_day_of_week = data['description']['day_of_week']
        if 'event_opened' in data['description']:
            inc.incident_event_opened = data['description']['event_opened']
        if 'event_closed' in data['description']:
            inc.incident_event_closed = data['description']['event_closed']

    if 'apparatus' in data:
        tmp_array = []
        for car in data['apparatus']:
            tmp_array.append('{} - {}/{}/{}/{}'.format(
                car['unit_type'],
                car['extended_data']['event_duration'],
                car['extended_data']['response_duration'],
                car['extended_data']['travel_duration'],
                car['extended_data']['turnout_duration']
            ))
        if tmp_array:
            inc.incident_units_involved = flat_points = '\n'.join([str(s) for s in tmp_array])
    return inc


def _read_from_file(fname):
    with open(fname, 'r') as json_file:
        return json.load(json_file)