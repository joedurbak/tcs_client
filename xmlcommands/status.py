import os.path
import datetime as dt
from pytz import timezone

from astropy.time import Time
from pandas import to_datetime
from xmltodict import parse

default_status_xml = os.path.join(os.path.basename(__file__), 'simulation', 'consumer.xml')


def time_to_total_seconds(time_object):
    return (dt.timedelta(
        hours=time_object.hour, minutes=time_object.minute, seconds=time_object.second,
        microseconds=time_object.microsecond)).total_seconds()


def dms_to_degrees(degrees, minutes, seconds):
    sign = 1
    if (degrees < 0) or (minutes < 0) or (seconds < 0):
        sign = -1
    return sign * (abs(degrees) + abs(minutes)/60 + abs(seconds)/3600)


def dms_to_seconds(degrees, minutes, seconds):
    return 3600 * dms_to_degrees(degrees, minutes, seconds)


def hms_to_arcseconds(hours, minutes, seconds):
    return (hours*3600 + minutes*60 + seconds) * 360/24


def xml_tag_loader(xml_dictionary, key_tuple):
    try:
        value = xml_dictionary.copy()
    except AttributeError:
        value = xml_dictionary
    for key in key_tuple:
        try:
            value = value[key]
        except KeyError:
            return ""
        except TypeError:
            if type(value) is list:
                try:
                    value = value[0][key]
                except KeyError or TypeError:
                    return ""
            else:
                return ""
    return value


class Status:
    def __init__(self, status_xml_file=default_status_xml, telescope_timezone='MST'):
        self.request_number_dict = {
            1: 'not implemented yet',  # Current date
            2: 'not implemented yet',  # UTC date
            3: 'not implemented yet',  # JD (Julian Day)
            4: 'not implemented yet',  # Current time
            5: 'not implemented yet',  # Current time (String)
            6: 'not implemented yet',  # UTC time
            7: 'not implemented yet',  # UTC time (String)
            8: 'not implemented yet',  # Difference between UT1 and UTC
            9: 'not implemented yet',  # Current local sidereal time
            10: 'not implemented yet',  # Current azimuth (arcsec)
            11: 'not implemented yet',  # Current azimuth (°)
            12: 'not implemented yet',  # Current elevation (arcsec)
            13: 'not implemented yet',  # Current elevation (°)
            14: 'not implemented yet',  # Current rotator angle (arcsec)
            15: 'not implemented yet',  # Current rotator angle (°)
            18: 'not implemented yet',  # Current RA
            19: 'not implemented yet',  # Current RA (String)
            20: 'not implemented yet',  # Current Dec
            21: 'not implemented yet',  # Current Dec (String)
            22: 'not implemented yet',  # secZ TODO: figure out what this is
            # TODO: figure out what T-Point correction is
            23: 'not implemented yet',  # Current RA without considering T-Point correction
            24: 'not implemented yet',  # Current Dec without considering T-Point correction
            # TODO: document that focus position isn't part of LDT status
            25: 'not implemented yet',  # Focus Position (A)
            26: 'not implemented yet',  # Focus Position (B)
            27: 'not implemented yet',  # Focus Position (A-B)
            16: 'not implemented yet',  # Current Error
            17: 'not implemented yet',  # Current Status
            370: 'not implemented yet',  # Extended Status
            90: 'not implemented yet',  # Observation ready flag
            50: 'not implemented yet',  # Offset 1 (RA)
            51: 'not implemented yet',  # Offset 1 (Dec)
            52: 'not implemented yet',  # Offset 1 (Azimuth)
            53: 'not implemented yet',  # Offset 1 (Altitude)
            54: 'not implemented yet',  # Offset 1 (Rotator)（°）
            78: 'not implemented yet',  # Offset 1 (time)
            120: 'not implemented yet',  # Current dome angle
            121: 'not implemented yet',  # Dome status
        }
        self.error_codes = {
            'none': 0,
            'hardware failure': 1,
            'backup data error': 2,
            'shutdown error': 3,
            'pc communication error': 4,
            'gps communication error': 5,
            'check sum error': 6,
            'zero search is required': 10,
            'cannot process until motors stop': 11,
            'emergency stop button pressed': 12,
            'failed to read absolute encoder': 13,
            'power driver unit off': 14,
            'failed to initialize x-axis': 100,
            'failed to initialize y-axis': 110,
            'failed to initialize theta-axis': 120,
            'x driver failure': 101,
            'y driver failure': 111,
            'theta driver error': 121,
        }
        self.status_xml_file = status_xml_file
        self.xml_dict = parse(self.status_xml_file)
        self.timezone = telescope_timezone
        self.load_datetime_values()
        self.load_coordinates()
        self.load_error()
        self.load_status()
        self.load_extended_status()
        self.load_observation_ready_flag()
        self.load_offsets()
        self.load_current_dome_angle()
        self.load_dome_status()

    def load_datetime_values(self):
        time_string = xml_tag_loader(self.xml_dict, ('tcsTCSStatus', 'currentTimes', 'time'))
        local_sidereal_time_dict = xml_tag_loader(self.xml_dict, ('tcsTCSStatus', 'currentTimes', 'lst'))
        local_sidereal_hour = xml_tag_loader(local_sidereal_time_dict, ('hours', ))
        local_sidereal_minutes = xml_tag_loader(local_sidereal_time_dict, ('minutesTime', ))
        local_sidereal_seconds = xml_tag_loader(local_sidereal_time_dict, ('secondsTime',))
        sidereal_time = dt.timedelta(
            hours=local_sidereal_hour, minutes=local_sidereal_minutes, seconds=local_sidereal_seconds
        ).total_seconds()
        utc_datetime = to_datetime(time_string, utc=True)
        tz = timezone(self.timezone).localize(utc_datetime)
        local_datetime = utc_datetime.replace(tzinfo=tz)
        astropy_time = Time(utc_datetime)
        self.request_number_dict[1] = local_datetime.date()
        self.request_number_dict[2] = utc_datetime.date()
        self.request_number_dict[3] = astropy_time.jd
        self.request_number_dict[4] = time_to_total_seconds(local_datetime.time())
        self.request_number_dict[5] = str(local_datetime.time())
        self.request_number_dict[6] = time_to_total_seconds(utc_datetime.time())
        self.request_number_dict[7] = str(utc_datetime.time())
        self.request_number_dict[8] = float(astropy_time.delta_ut1_utc)
        self.request_number_dict[9] = sidereal_time

    def load_coordinates(self):
        pointing_dict = xml_tag_loader(self.xml_dict, ('tcsTCSStatus', 'pointingPositions'))
        azimuth_dict = xml_tag_loader(pointing_dict, ('currentAzEl', 'azimuth'))
        azimuth_degrees = xml_tag_loader(azimuth_dict, ('degreesArc',))
        azimuth_minutes = xml_tag_loader(azimuth_dict, ('minutesArc',))
        azimuth_seconds = xml_tag_loader(azimuth_dict, ('secondsArc',))
        self.request_number_dict[10] = dms_to_seconds(azimuth_degrees, azimuth_minutes, azimuth_seconds)
        self.request_number_dict[11] = dms_to_degrees(azimuth_degrees, azimuth_minutes, azimuth_seconds)
        elevation_dict = xml_tag_loader(pointing_dict, ('currentAzEl', 'azimuth'))
        elevation_degrees = xml_tag_loader(elevation_dict, ('degreesAlt', ))
        elevation_minutes = xml_tag_loader(elevation_dict, ('minutesArc',))
        elevation_seconds = xml_tag_loader(elevation_dict, ('secondsArc',))
        self.request_number_dict[12] = dms_to_seconds(elevation_degrees, elevation_minutes, elevation_seconds)
        self.request_number_dict[13] = dms_to_seconds(elevation_degrees, elevation_minutes, elevation_seconds)
        rotator_angle_degrees = xml_tag_loader(pointing_dict, ('currentRotatorPositions', 'rotPA'))
        self.request_number_dict[14] = rotator_angle_degrees * 3600
        self.request_number_dict[15] = rotator_angle_degrees
        ra_hours = xml_tag_loader(pointing_dict, ('currentRADec', 'ra', 'hours'))
        ra_minutes = xml_tag_loader(pointing_dict, ('currentRADec', 'ra', 'minutesTime'))
        ra_seconds = xml_tag_loader(pointing_dict, ('currentRADec', 'ra', 'secondsTime'))
        self.request_number_dict[18] = hms_to_arcseconds(ra_hours, ra_minutes, ra_seconds)
        self.request_number_dict[19] = "{}:{}:{}".format(ra_hours, ra_minutes, ra_seconds)
        dec_degrees = xml_tag_loader(pointing_dict, ('currentRADec', 'declination', 'degreesDec'))
        dec_minutes = xml_tag_loader(pointing_dict, ('currentRADec', 'declination', 'minutesArc'))
        dec_seconds = xml_tag_loader(pointing_dict, ('currentRADec', 'declination', 'secondsArc'))
        self.request_number_dict[20] = dms_to_seconds(dec_degrees, dec_minutes, dec_seconds)
        self.request_number_dict[21] = "{}:{}:{}".format(dec_degrees, dec_minutes, dec_seconds)
        self.request_number_dict[22] = xml_tag_loader(
            self.xml_dict, ('tcsTCSStatus', 'limits', 'zenith', 'currentZD_deg')
        )

    def load_error(self):
        pass

    def load_status(self):
        pass

    def load_extended_status(self):
        pass

    def load_observation_ready_flag(self):
        pass

    def load_offsets(self):
        pass

    def load_current_dome_angle(self):
        pass

    def load_dome_status(self):
        pass
