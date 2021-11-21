"""
django models to define Parcel and Incident
"""
from django.db import models

class Parcel(models.Model):
    '''
    parcel enrichment
    '''
    parcel_owner_name = models.CharField(max_length=100, default='')
    parcel_mail_address = models.TextField(default='')
    parcel_land_value = models.FloatField(default='')
    parcel_land_sq_ft = models.FloatField(default='')

    # TODO: change to array.
    parcel_polygon_string_list = models.TextField(default='')

    def __str__(self):
        return 'PARCEL: {} - {} - {} - {}'.format(
            self.parcel_owner_name,
            self.parcel_mail_address,
            self.parcel_land_value,
            self.parcel_land_sq_ft
            )

    def get_polygon(self):
        """return array of arrays of lat/lng"""
        ret_array = []
        if self.parcel_polygon_string_list:
            cur_array = []
            for num in str(self.parcel_polygon_string_list).split(','):
                cur_array.append(float(num))
                if len(cur_array) == 2:
                    ret_array.append(cur_array.copy())
                    cur_array = []
        return ret_array

class Incident(models.Model):
    '''
    I'm taking the most interesting parts of the incidents to show
    and mapping them to a field in the db.
    '''
    incident_number = models.CharField(max_length=12, primary_key=True)

    # taken from address
    incident_latitude = models.FloatField(default=0.0)
    incident_longitude = models.FloatField(default=0.0)

    # concatted value for display.
    incident_address_string = models.CharField(max_length=200, default='')

    # TODO: change to enums
    incident_type = models.CharField(max_length=100, default='')
    incident_sub_type = models.CharField(max_length=100, default='')
    incident_day_of_week = models.CharField(max_length=8, default='')

    incident_event_opened = models.DateTimeField(auto_now_add=False, default='')
    incident_event_closed = models.DateTimeField(auto_now_add=False, default='')
    incident_response_zone = models.CharField(max_length=10, default='')
    incident_parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE)

    # TODO: change to array
    incident_units_involved = models.CharField(max_length=200, default='')

    '''
    there are others we can add here, like all the different
    units that responded.
    '''

    # Enrichment
    # -- Weather
    incident_weather_description = models.TextField(default='')

    def __str__(self):
        return 'INCIDENT: {} - {} - {} - {} - {} - {}'.format(
            self.incident_number,
            self.incident_latitude,
            self.incident_longitude,
            self.incident_parcel,
            self.incident_type,
            self.incident_sub_type
            )

    def get_response_unit_stats(self):
        '''
        There's a better way to store this data in the DB,
        but in the interest of time, I'm parsing the string
        here so it can be better rendered.
        '''

        if not self.incident_units_involved:
            return []

        ret_array = []
        units = str(self.incident_units_involved).split('\n')
        for unit in units:
            unit = unit.strip()
            unit_type = unit.split('-')[0].strip()
            unit_stats = unit.split('-')[1].strip()
            event_duration = unit_stats.split('/')[0]
            response_duration = unit_stats.split('/')[1]
            travel_duration = unit_stats.split('/')[2]
            turnout_duration = unit_stats.split('/')[3]
            ret_array.append({
                'unit_type': unit_type,
                'event_duration': event_duration,
                'response_duration': response_duration,
                'travel_duration': travel_duration,
                'turnout_duration': turnout_duration
            })
        return ret_array
