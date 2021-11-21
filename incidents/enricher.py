"""
enricher module that holds the Enricher class.
"""
import random
import pytz
import names
import requests
from .models import Parcel, Incident
from datetime import datetime

class Enricher():
    """Enricher Class
    This class processes the raw data that is needed as input to call
    the weather and arcgis apis.
    Controller classes instantiate this class and call the 'enrich'
    method to add enrichments to the model passed in.
    """
    def __init__(self, data):
        self.data = data
        self.weather_lat_long = []
        self.parcel_polygon_list = []

        self._set_weather_lat_long()
        self._set_parcel_polygon_list()

        #print('weather: {}'.format(self.weather_lat_long))
        #print('parcel: {}'.format(self.parcel_polygon_list))


    def enrich(self, _model_instance):
        """enrich
        Given the model instance, this method enriches it
        Throws exception if model instance is not supported.
        """
        if isinstance(_model_instance, Parcel):
            self._enrich_parcel(_model_instance)
        elif isinstance(_model_instance, Incident):
            self._enrich_incident(_model_instance)
        else:
            raise Exception('enrich does not support {}'.format(type(_model_instance)))

    def _iso_to_utc_epoch(self, iso):
        # TODO: make this timezone calculation better.
        _tz = pytz.timezone('UTC')
        offset = 0 - int(iso[:-3][-3:]) * 3600
        dt_with_tz = _tz.localize(datetime.strptime(iso[:-6], '%Y-%m-%dT%H:%M:%S'), is_dst=None)
        _ts = (dt_with_tz - datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds() + offset
        return int(_ts)

    def _enrich_incident(self, incident):
        flat_points = ','.join([str(s) for s in self.weather_lat_long])
        weather_ts = incident.incident_event_opened
        url = 'https://api.darksky.net/forecast/971bc3c7f3e0e07dc4982e2aa9f013f9' \
              '/{},{}?exclude=currently,flags,daily'.format(flat_points, weather_ts)
        print('_enrich_incident request url is: {}'.format(url))
        response = requests.get(url)
        print('_enrich_incident response is: {}'.format(response.json()))

        # check each hourly and check the weather of the closest half-hour to incident
        try:
            body = response.json()
        except Exception as _e:
            raise _e

        incident_epoch = self._iso_to_utc_epoch(weather_ts)

        if 'hourly' in body and 'data' in body['hourly']:
            incident.weather_description = 'No Weather Data'
            for hour in body['hourly']['data']:
                if abs(hour['time'] - incident_epoch) < (30*60):
                    # found the incident weather
                    incident.incident_weather_description = self._get_weather_description(hour)
                    break


    def _get_weather_description(self, weather_data):
        # TODO: add dew point and apparent temp later.
        temperature = weather_data['temperature'] if 'temperature' in weather_data else ''
        summary = weather_data['summary'] if 'summary' in weather_data else ''
        p_intensity = weather_data['precipIntensity'] if 'precipIntensity' in weather_data else ''
        p_probability = weather_data['precipProbability'] if \
                'precipProbability' in weather_data else ''
        humidity = weather_data['humidity'] if 'humidity' in weather_data else ''
        pressure = weather_data['pressure'] if 'pressure' in weather_data else ''
        wspeed = weather_data['windSpeed'] if 'windSpeed' in weather_data else ''
        wgust = weather_data['windGust'] if 'windGust' in weather_data else ''
        wbearing = weather_data['windBearing'] if 'windBearing' in weather_data else ''
        cloudcover = weather_data['cloudCover'] if 'cloudCover' in weather_data else ''
        uvindex = weather_data['uvIndex'] if 'uvIndex' in weather_data else ''
        visibility = weather_data['visibility'] if 'visibility' in weather_data else ''
        return '{} degrees and {}<br>PrecipIntensity: {}<br>PrecipProbability: {}' \
                '<br>Humidity: {}<br>Pressure: {}<br>Wind Speed: {}<br>Wind Gust: {}'\
                '<br>Wind Bearing: {}<br>Cloud Cover: {}<br>UV Index: {}<br>Visibility: {}'\
                .format(temperature, summary, p_intensity, p_probability,
                        humidity, pressure, wspeed, wgust, wbearing,
                        cloudcover, uvindex, visibility)


    # SOMETHING WRONG HERE.... Need to fix API.
    def _enrich_parcel(self, parcel):
        flat_points = ','.join([str(s) for s in self.parcel_polygon_list])
        url = 'http://gis.richmondgov.com/ArcGIS/rest/services/StatePlane4502/' \
              'Ener/MapServer/0/query?text=&geometry={}&inSR=&spatialRel=' \
              'esriSpatialRelIntersects&relationParam=&objectIds=&where=&time=' \
              '&returnCountOnly=false&returnIdsOnly=false&returnGeometry=true&' \
              'maxAllowableOffset=&outSR=&outFields=&f=json'.format(flat_points)
        print('_enrich_parcel request url is: {}'.format(url))
        # response = requests.get(url)
        # print('_enrich_parcel response is: {}'.format(response.json()))

        # Since i'm not getting good data from the API... gonna fake this up.

        # Add the owners name
        parcel.parcel_owner_name = names.get_full_name()

        # Add mail address --
        # TODO: not being used due to API issue.
        parcel.parcel_mail_address = '{} {} {}'.format(
            random.randrange(1, 300), names.get_first_name(),
            random.choice(['St.', 'Ave.', 'Blvd.', 'Way',
                           'Crossing', 'Rd', 'Pkwy']))

        # Add land value
        parcel.parcel_land_value = random.randrange(80000, 650000, 50)

        # Add land sq ft
        parcel.parcel_land_sq_ft = random.randrange(600, 6500, 15)

        # copy the polygon
        new_poly = self.parcel_polygon_list.copy()
        new_poly.reverse()
        parcel.parcel_polygon_string_list = ','.join([str(s) for s in new_poly])

    def _set_weather_lat_long(self):
        if 'address' in self.data and \
            'latitude' in self.data['address'] and \
            'longitude' in self.data['address']:

            self.weather_lat_long = [
                self.data['address']['latitude'],
                self.data['address']['longitude']
            ]
        else:
            raise Exception('lat/long not found in address. Check file')

    def _set_parcel_polygon_list(self):
        '''
        To determine polygon for query:
            - incident address lat/long
            - for each unit's arrival lat/long
        Output: keep it simple, just a list of lat longs.
        (longitude first) -- so long/lats as specified in the API
        '''
        if self.weather_lat_long:
            # put in reverse order for api
            self.parcel_polygon_list.append(self.weather_lat_long[1])
            self.parcel_polygon_list.append(self.weather_lat_long[0])

        if 'apparatus' in self.data and len(self.data['apparatus']) > 2:
            # add to polygon
            apparatus = self.data['apparatus']
            for car in apparatus:
                if 'unit_status' in car and \
                        'arrived' in car['unit_status'] and \
                        'longitude' in car['unit_status']['arrived'] and \
                        'latitude' in car['unit_status']['arrived']:
                    self.parcel_polygon_list.append(car['unit_status']['arrived']['longitude'])
                    self.parcel_polygon_list.append(car['unit_status']['arrived']['latitude'])
        else:
            if 'apparatus' in self.data and self.data['apparatus']:
                car = self.data['apparatus'][0]
                self.parcel_polygon_list.append(car['unit_status']['dispatched']['longitude'])
                self.parcel_polygon_list.append(car['unit_status']['dispatched']['latitude'])
            else:
                raise Exception('Not enough data to create a polygon for parcel')