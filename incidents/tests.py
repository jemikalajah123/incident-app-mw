"""
Django Testing
Approach: Since this django project is not model-heavy. I've
chosen to test mostly using client.get('/') and inspecting the
html output
"""
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Parcel, Incident
import json

'''
TODO: break these out into separate files
'''

### General ###
class IndexViewTests(TestCase):
    """ IndexViewTests """

    def test_page_loads(self):
        """ verify page loads """
        response = self.client.get('/')
        content = response.content.decode('utf-8')
        self.assertTrue(response.status_code == 200)
        self.assertTrue('Test Code for Prominent Edge' in content)


    # test uploading file
    def test_upload_file1(self):
        """ test_upload_file1
        The most generic test but covers the most ground.
        A sanity test.
        """
        myfile = SimpleUploadedFile("testfile.json", file_content, content_type="application/json")
        response = self.client.post('/', {'myfile': myfile})
        #print(response.content)
        self.assertTrue(response.status_code == 200)
        content = response.content.decode('utf-8')
        self.assertTrue('Address: 333 E FRANKLIN ST' in content)
        self.assertTrue('Incident Number: F01705150050' in content)
        self.assertTrue('HAZMAT => SMELL OR ODOR (NO SPILL)' in content)

        # test for weather enrichment
        self.assertTrue('degrees and' in content)
        self.assertTrue('Incident Opened: 20' in content)
        self.assertTrue('Incident Closed: 20' in content)
        self.assertTrue('PrecipProbability:' in content)
        self.assertTrue('Humidity:' in content)
        self.assertTrue('Wind Speed:' in content)

        # test for parcel
        self.assertTrue('L.polygon([[' in content)



### Parcel Tests ###
class ParcelTests(TestCase):
    """ ParcelTests """

    # test missing parcel owner name
    def test_missing_parcel_owner_name(self):
        """test_missing_parcel_owner_name"""
        delete_entries()
        _json = json.loads(file_content.decode('utf-8'))
        _json['description'].pop('incident_number')
        myfile = SimpleUploadedFile("testfile.json",
                                    str.encode(json.dumps(_json)),
                                    content_type="application/json")
        response = self.client.post('/', {'myfile': myfile})
        #print(response.content)
        self.assertTrue(response.status_code == 200)
        content = response.content.decode('utf-8')
        self.assertTrue('Cannot find incident_number.' in content)


    # test missing parcel mail address
    def test_missing_parcel_mail_address(self):
        """
        My implementation allows for rendering even with missing address.
        """
        delete_entries()
        _json = json.loads(file_content.decode('utf-8'))
        _json['address'].pop('address_line1')
        myfile = SimpleUploadedFile("testfile.json",
                                    str.encode(json.dumps(_json)),
                                    content_type="application/json")
        response = self.client.post('/', {'myfile': myfile})
        #print(response.content)
        self.assertTrue(response.status_code == 200)
        content = response.content.decode('utf-8')
        self.assertTrue('Address: </p>' in content)

    # test missing parcel land value
    def test_exists_parcel_land_value(self):
        """
        Right now, this can never be missing. so test for existence.
        """
        delete_entries()
        myfile = SimpleUploadedFile("testfile.json",
                                    file_content,
                                    content_type="application/json")
        response = self.client.post('/', {'myfile': myfile})
        #print(response.content)
        self.assertTrue(response.status_code == 200)
        content = response.content.decode('utf-8')
        self.assertTrue('Land Value: </p>' not in content)
        self.assertTrue('Land Value:' in content)

    # test missing parcel land sq ft
    def test_exists_parcel_land_sqft(self):
        """
        Right now, this can never be missing. so test for existence.
        """
        delete_entries()
        myfile = SimpleUploadedFile("testfile.json",
                                    file_content,
                                    content_type="application/json")
        response = self.client.post('/', {'myfile': myfile})
        #print(response.content)
        self.assertTrue(response.status_code == 200)
        content = response.content.decode('utf-8')
        self.assertTrue('Land Area: </p>' not in content)
        self.assertTrue('Land Area:' in content)

    # test missing parcel polygon string list
    def test_missing_parcel_polygon_string_list(self):
        """test_missing_parcel_polygon_string_list"""
        delete_entries()
        _json = json.loads(file_content.decode('utf-8'))
        _json['apparatus'] = []
        myfile = SimpleUploadedFile("testfile.json",
                                    str.encode(json.dumps(_json)),
                                    content_type="application/json")
        response = self.client.post('/', {'myfile': myfile})
        #print(response.content)
        self.assertTrue(response.status_code == 200)
        content = response.content.decode('utf-8')
        self.assertTrue('L.polygon()' in content)
        self.assertTrue('L.marker([, ]).addTo(mymap)' in content)


### Incident Tests ###
class IncidentTests(TestCase):
    """ IncidentTests """

    # test missing lat
    def test_missing_incident_lat(self):
        """test_missing_incident_lat"""
        delete_entries()
        _json = json.loads(file_content.decode('utf-8'))
        _json['address'].pop('latitude')
        myfile = SimpleUploadedFile("testfile.json",
                                    str.encode(json.dumps(_json)),
                                    content_type="application/json")
        response = self.client.post('/', {'myfile': myfile})
        #print(response.content)
        self.assertTrue(response.status_code == 200)
        content = response.content.decode('utf-8')
        self.assertTrue('Error Message: lat/long not found in address. Check file' in content)

    # test missing long
    def test_missing_incident_lng(self):
        """test_missing_incident_lng"""
        delete_entries()
        _json = json.loads(file_content.decode('utf-8'))
        _json['address'].pop('longitude')
        myfile = SimpleUploadedFile("testfile.json",
                                    str.encode(json.dumps(_json)),
                                    content_type="application/json")
        response = self.client.post('/', {'myfile': myfile})
        #print(response.content)
        self.assertTrue(response.status_code == 200)
        content = response.content.decode('utf-8')
        self.assertTrue('Error Message: lat/long not found in address. Check file' in content)

    # test missing type
    def test_missing_type(self):
        """test_missing_type"""
        delete_entries()
        _json = json.loads(file_content.decode('utf-8'))
        _json['description'].pop('type')
        myfile = SimpleUploadedFile("testfile.json",
                                    str.encode(json.dumps(_json)),
                                    content_type="application/json")
        response = self.client.post('/', {'myfile': myfile})
        #print(response.content)
        self.assertTrue(response.status_code == 200)
        content = response.content.decode('utf-8')
        self.assertTrue('Incident Type:  =>' in content)

    # test missing sub type
    def test_missing_sub_type(self):
        """test_missing_sub_type"""
        delete_entries()
        _json = json.loads(file_content.decode('utf-8'))
        _json['description'].pop('subtype')
        myfile = SimpleUploadedFile("testfile.json",
                                    str.encode(json.dumps(_json)),
                                    content_type="application/json")
        response = self.client.post('/', {'myfile': myfile})
        #print(response.content)
        self.assertTrue(response.status_code == 200)
        content = response.content.decode('utf-8')
        self.assertTrue('Incident Type: HAZMAT => </p>' in content)

    # test missing day of week
    def test_missing_day_of_week(self):
        """test_missing_day_of_week"""
        delete_entries()
        _json = json.loads(file_content.decode('utf-8'))
        _json['description'].pop('day_of_week')
        myfile = SimpleUploadedFile("testfile.json",
                                    str.encode(json.dumps(_json)),
                                    content_type="application/json")
        response = self.client.post('/', {'myfile': myfile})
        #print(response.content)
        self.assertTrue(response.status_code == 200)
        content = response.content.decode('utf-8')
        self.assertTrue('Monday, ' not in content)

    # test missing event opened
    def test_missing_event_opened(self):
        """test_missing_event_opened"""
        delete_entries()
        _json = json.loads(file_content.decode('utf-8'))
        _json['description'].pop('event_opened')
        myfile = SimpleUploadedFile("testfile.json",
                                    str.encode(json.dumps(_json)),
                                    content_type="application/json")
        response = self.client.post('/', {'myfile': myfile})
        #print(response.content)
        self.assertTrue(response.status_code == 200)
        content = response.content.decode('utf-8')
        self.assertTrue('Incident Opened: </p>' in content)

    # test missing event closed
    def test_missing_event_closed(self):
        """test_missing_event_closed"""
        delete_entries()
        _json = json.loads(file_content.decode('utf-8'))
        _json['description'].pop('event_closed')
        myfile = SimpleUploadedFile("testfile.json",
                                    str.encode(json.dumps(_json)),
                                    content_type="application/json")
        response = self.client.post('/', {'myfile': myfile})
        #print(response.content)
        self.assertTrue(response.status_code == 200)
        content = response.content.decode('utf-8')
        self.assertTrue(
            'value has an invalid format. It must be in YYYY-MM-DD' in content)

    # test missing response zone
    def test_missing_response_zone(self):
        """test_missing_response_zone"""
        delete_entries()
        _json = json.loads(file_content.decode('utf-8'))
        _json['address'].pop('response_zone')
        myfile = SimpleUploadedFile("testfile.json",
                                    str.encode(json.dumps(_json)),
                                    content_type="application/json")
        response = self.client.post('/', {'myfile': myfile})
        #print(response.content)
        self.assertTrue(response.status_code == 200)
        content = response.content.decode('utf-8')
        self.assertTrue('Response Zone: </p>' in content)

    # add more tests here.



file_content = b'''{
    "address": {
        "address_id": "", 
        "address_line1": "333 E FRANKLIN ST", 
        "city": "Richmond", 
        "common_place_name": "MEDIA GENERAL - TIMES DISPATCH", 
        "cross_street1": "N 3RD ST", 
        "cross_street2": "N 4TH ST", 
        "first_due": "6", 
        "geohash": "dq8vtf33qdte", 
        "latitude": 37.541885, 
        "longitude": -77.440624, 
        "name": "FRANKLIN", 
        "number": "333", 
        "postal_code": "", 
        "prefix_direction": "E", 
        "response_zone": "701601", 
        "state": "VA", 
        "suffix_direction": "", 
        "type": "ST"
    }, 
    "apparatus": [
        {
            "car_id": "891284", 
            "extended_data": {
                "event_duration": 4134, 
                "response_duration": 762, 
                "travel_duration": 504, 
                "turnout_duration": 258
            }, 
            "geohash": "dq8vhztwn5ym", 
            "personnel": [], 
            "shift": "B", 
            "station": "FSTA22", 
            "unit_id": "H3", 
            "unit_status": {
                "acknowledged": {
                    "geohash": "dq8vhztwn5ym", 
                    "latitude": 37.483656, 
                    "longitude": -77.478753, 
                    "timestamp": "2017-05-15T13:21:38-04:00"
                }, 
                "arrived": {
                    "geohash": "dq8vtf33qdte", 
                    "latitude": 37.541885, 
                    "longitude": -77.440624, 
                    "timestamp": "2017-05-15T13:32:12-04:00"
                }, 
                "available": {
                    "geohash": "dq8vtf33qdte", 
                    "latitude": 37.541885, 
                    "longitude": -77.440624, 
                    "timestamp": "2017-05-15T14:28:24-04:00"
                }, 
                "cleared": {
                    "geohash": "dq8vhztwn5ym", 
                    "latitude": 37.483656, 
                    "longitude": -77.478753, 
                    "timestamp": "2017-05-15T13:32:04-04:00"
                }, 
                "dispatched": {
                    "geohash": "dq8vhztwn5ym", 
                    "latitude": 37.483656, 
                    "longitude": -77.478753, 
                    "timestamp": "2017-05-15T13:19:30-04:00"
                }, 
                "enroute": {
                    "geohash": "dq8vhztwn5ym", 
                    "latitude": 37.483656, 
                    "longitude": -77.478753, 
                    "timestamp": "2017-05-15T13:23:48-04:00"
                }, 
                "~": {
                    "geohash": "dq8vhztwn5ym", 
                    "latitude": 37.483656, 
                    "longitude": -77.478753, 
                    "timestamp": "2017-05-15T13:31:48-04:00"
                }
            }, 
            "unit_type": "Hazmat Unit"
        }, 
        {
            "car_id": "121310", 
            "extended_data": {
                "event_duration": 4132, 
                "response_duration": 762, 
                "travel_duration": 713, 
                "turnout_duration": 49
            }, 
            "geohash": "dq8vhztwm8pw", 
            "personnel": [], 
            "shift": "B", 
            "station": "FSTA22", 
            "unit_id": "T22", 
            "unit_status": {
                "arrived": {
                    "geohash": "dq8vtf27fxu9", 
                    "latitude": 37.542342, 
                    "longitude": -77.44217, 
                    "timestamp": "2017-05-15T13:32:12-04:00"
                }, 
                "available": {
                    "geohash": "dq8vhzubkktu", 
                    "latitude": 37.484046, 
                    "longitude": -77.479859, 
                    "timestamp": "2017-05-15T14:28:22-04:00"
                }, 
                "cleared": {
                    "geohash": "dq8vmqkemjqy", 
                    "latitude": 37.520271, 
                    "longitude": -77.458196, 
                    "timestamp": "2017-05-15T13:28:25-04:00"
                }, 
                "dispatched": {
                    "geohash": "dq8vhztwm8pw", 
                    "latitude": 37.483679, 
                    "longitude": -77.478773, 
                    "timestamp": "2017-05-15T13:19:30-04:00"
                }, 
                "enroute": {
                    "geohash": "dq8vhztwm8pw", 
                    "latitude": 37.483679, 
                    "longitude": -77.478773, 
                    "timestamp": "2017-05-15T13:20:19-04:00"
                }, 
                "~": {
                    "geohash": "dq8vmq5rwvb8", 
                    "latitude": 37.519629, 
                    "longitude": -77.459846, 
                    "timestamp": "2017-05-15T13:28:19-04:00"
                }
            }, 
            "unit_type": "Truck/Aerial"
        }, 
        {
            "car_id": "161330", 
            "extended_data": {
                "event_duration": 5234, 
                "response_duration": 769, 
                "travel_duration": 688, 
                "turnout_duration": 81
            }, 
            "geohash": "dq8vhztwr80y", 
            "personnel": [], 
            "shift": "B", 
            "station": "FSTA22", 
            "unit_id": "E22", 
            "unit_status": {
                "arrived": {
                    "geohash": "dq8vmwb9qrb6", 
                    "latitude": 37.522687, 
                    "longitude": -77.452658, 
                    "timestamp": "2017-05-15T13:32:20-04:00"
                }, 
                "available": {
                    "geohash": "dq8vhztwjff9", 
                    "latitude": 37.48365, 
                    "longitude": -77.478769, 
                    "timestamp": "2017-05-15T14:46:45-04:00"
                }, 
                "cleared": {
                    "geohash": "dq8vmwb9qrb6", 
                    "latitude": 37.522687, 
                    "longitude": -77.452658, 
                    "timestamp": "2017-05-15T13:29:02-04:00"
                }, 
                "dispatched": {
                    "geohash": "dq8vhztwr80y", 
                    "latitude": 37.483679, 
                    "longitude": -77.478696, 
                    "timestamp": "2017-05-15T13:19:31-04:00"
                }, 
                "enroute": {
                    "geohash": "dq8vhztwr80y", 
                    "latitude": 37.483679, 
                    "longitude": -77.478696, 
                    "timestamp": "2017-05-15T13:20:52-04:00"
                }, 
                "~": {
                    "geohash": "dq8vmwb9qrb6", 
                    "latitude": 37.522687, 
                    "longitude": -77.452658, 
                    "timestamp": "2017-05-15T13:28:52-04:00"
                }
            }, 
            "unit_type": "Engine"
        }, 
        {
            "car_id": "091299", 
            "extended_data": {
                "event_duration": 4143, 
                "response_duration": 761, 
                "travel_duration": 508, 
                "turnout_duration": 253
            }, 
            "geohash": "dq8vhztwn5ym", 
            "personnel": [], 
            "shift": "B", 
            "station": "FSTA22", 
            "unit_id": "H2", 
            "unit_status": {
                "acknowledged": {
                    "geohash": "dq8vhztwn5ym", 
                    "latitude": 37.483656, 
                    "longitude": -77.478753, 
                    "timestamp": "2017-05-15T13:21:36-04:00"
                }, 
                "arrived": {
                    "geohash": "dq8vtf33qdte", 
                    "latitude": 37.541885, 
                    "longitude": -77.440624, 
                    "timestamp": "2017-05-15T13:32:12-04:00"
                }, 
                "available": {
                    "geohash": "dq8vtf33qdte", 
                    "latitude": 37.541885, 
                    "longitude": -77.440624, 
                    "timestamp": "2017-05-15T14:28:34-04:00"
                }, 
                "cleared": {
                    "geohash": "dq8vhztwn5ym", 
                    "latitude": 37.483656, 
                    "longitude": -77.478753, 
                    "timestamp": "2017-05-15T13:32:04-04:00"
                }, 
                "dispatched": {
                    "geohash": "dq8vhztwn5ym", 
                    "latitude": 37.483656, 
                    "longitude": -77.478753, 
                    "timestamp": "2017-05-15T13:19:31-04:00"
                }, 
                "enroute": {
                    "geohash": "dq8vhztwn5ym", 
                    "latitude": 37.483656, 
                    "longitude": -77.478753, 
                    "timestamp": "2017-05-15T13:23:44-04:00"
                }, 
                "~": {
                    "geohash": "dq8vhztwn5ym", 
                    "latitude": 37.483656, 
                    "longitude": -77.478753, 
                    "timestamp": "2017-05-15T13:31:44-04:00"
                }
            }, 
            "unit_type": "Hazmat Unit"
        }
    ], 
    "description": {
        "comments": "** LOI search completed at 05/15/17 13:19:12 SPECIAL ADDRESS COMMENT: ***RFD: TARGET HAZARD*** ** Case number C201713827 has been assigned to event F01705150050 ** >>>> by: NANCY L. MOREY on terminal: ecc-f1 OLD BOX OF CHEMICALS WANTS IT TO BE CHECKED OUT *****************TAC 3******************* T22/H2/H3 OS - LT FROM T22 HAS CMD", 
        "day_of_week": "Monday", 
        "event_closed": "2017-05-15T14:46:46-04:00", 
        "event_id": "3587288", 
        "event_opened": "2017-05-15T13:19:12-04:00", 
        "extended_data": {
            "dispatch_duration": 18, 
            "event_duration": 5254, 
            "response_time": 762
        }, 
        "first_unit_arrived": "2017-05-15T13:32:12-04:00", 
        "first_unit_dispatched": "2017-05-15T13:19:30-04:00", 
        "first_unit_enroute": "2017-05-15T13:20:19-04:00", 
        "hour_of_day": 13, 
        "incident_number": "F01705150050", 
        "loi_search_complete": "2017-05-15T13:19:12-04:00", 
        "subtype": "SMELL OR ODOR (NO SPILL)", 
        "type": "HAZMAT"
    }, 
    "fire_department": {
        "fd_id": "76000", 
        "firecares_id": "93345", 
        "name": "Richmond Fire and Emergency Services", 
        "shift": "B", 
        "state": "VA", 
        "timezone": "US/Eastern"
    }, 
    "version": "1.0.29"
}
'''


def delete_entries():
    """helper to delete objects"""
    Parcel.objects.all().delete()
    Incident.objects.all().delete()
