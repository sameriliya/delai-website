import requests
import pandas as pd
import numpy as np
import datetime
import os
from dateutil import tz

def get_raw_flight_details(flight_number='UAL4', date=datetime.date.today()):
    '''Enter a flight number e.g UAL4, and a date of travel and return a json blob
    containing flight details from the FlightAware API.
    The data will be raw and in need of post processing using other functions.
    '''
    AEROAPI_BASE_URL = "https://aeroapi.flightaware.com/aeroapi/flights/"
    AEROAPI_KEY = os.environ.get("FA_API_KEY")
    AEROAPI = requests.Session()
    AEROAPI.headers.update({"x-apikey": AEROAPI_KEY})

    start = date
    end = date + datetime.timedelta(days = 1)

    full_url = AEROAPI_BASE_URL + flight_number
    params = {'start':start,
              'end':end
             }

    response = AEROAPI.get(full_url, params = params)
    return response

def localize_time(time, timezone):
    '''Helper function to localize UTC datetime object when given a timezone
    '''
    to_zone = tz.gettz(timezone)
    return time.astimezone(to_zone)

def add_local_times(raw_details):
    '''
    Take raw flight details json blob and create columns with the the scheduled departure
    and arrival times, localized to the dep/arr locations to match the training data
    '''
    columns = ['scheduled_out',
           'scheduled_in',
           'operator_iata',
           'flight_number',
           'origin',
           'destination',
           'filed_ete',
           'route_distance']

    raw_details_df = pd.DataFrame(raw_details)[columns]
    raw_details_df['scheduled_out'] = pd.to_datetime(raw_details_df['scheduled_out'])
    raw_details_df['scheduled_in'] = pd.to_datetime(raw_details_df['scheduled_in'])

    raw_details_df['origin_code'] = raw_details_df.origin[0]['code_iata']
    raw_details_df['origin_tz'] = raw_details_df.origin[0]['timezone']

    raw_details_df['dest_code'] = raw_details_df.destination[0]['code_iata']
    raw_details_df['dest_tz'] = raw_details_df.destination[0]['timezone']

    raw_details_df['scheduled_out_local'] = raw_details_df.apply(lambda raw_details: localize_time(raw_details.scheduled_out,
                                                       raw_details.origin_tz),
                                                       axis = 1)
    raw_details_df['scheduled_in_local'] = raw_details_df.apply(lambda raw_details: localize_time(raw_details.scheduled_in,
                                                      raw_details.dest_tz),
                                                      axis = 1)
    return raw_details_df


def extract_info_from_datetime_col(df):
    '''
    Given a dataframe of raw flight details, now in local time,
    extract year, month, day, weekday, and format local time of dep/arr.

    '''
    df['Year'] = df['scheduled_out_local'].dt.year
    df['Quarter'] = df['scheduled_out_local'].dt.quarter
    df['Month'] = df['scheduled_out_local'].dt.month
    df['DayofMonth'] = df['scheduled_out_local'].dt.day
    df['DayOfWeek'] = df['scheduled_out_local'].dt.dayofweek + 1
    df['CRSDepTime'] = df['scheduled_out_local'].dt.strftime('%H%M').astype(int)
    df['CRSArrTime'] = df['scheduled_in_local'].dt.strftime('%H%M').astype(int)
    df['FlightDate'] = df['scheduled_out_local'].dt.date
    return df


def clean_df(df):
    '''
    Get the output df we need to feed into model for preprocessing.
    Rename the columns where needed.
    '''
    columns = ['FlightDate',
               'Year',
               'Quarter',
               'Month',
               'DayofMonth',
               'DayOfWeek',
               'operator_iata', #turn into 'Marketing_Airline_Network'
               'origin_code', # change to Origin
               'dest_code', # change to Dest
               'CRSDepTime',
               'CRSArrTime',
               'route_distance' # change to 'Distance'
              ]
    df_out = df[columns]
    df_out = df_out.rename(columns = {'operator_iata':'Marketing_Airline_Network',
                             'origin_code':'Origin',
                             'dest_code':'Dest',
                             'route_distance':'Distance'})

    return df_out

def get_airport_details_dict(airport_code):
    AEROAPI_BASE_URL = "https://aeroapi.flightaware.com/aeroapi/airports/"
    AEROAPI_KEY = os.environ.get("FA_API_KEY")
    AEROAPI = requests.Session()
    AEROAPI.headers.update({"x-apikey": AEROAPI_KEY})

    full_url = AEROAPI_BASE_URL + airport_code

    response = AEROAPI.get(full_url,)

    response_json = response.json()

    if response.ok:
        name = response_json['name']
        location = f"{response_json['city']}, {response_json['state']}"
        lat = response_json['latitude']
        lon = response_json['longitude']
        return {'name':name, 'location':location, 'coord':[lon,lat]}
    else:
        print(response)
        print("Couldn't find airport")
        return {'name':'N/A', 'location':'N/A', 'coord':['N/A','N/A']}

def process_flight_details(response):
    '''Given a flight number and date of travel, use functions to
    return a cleaned dataframe of flight details to pass into an ML model
    '''

    if not response.ok:
        print('Add in actions for bad API call')
    if response.ok:
        flights = response.json()['flights']
        print(len(flights))
        if len(flights) == 0:
            print('Add action for no flights found')
            return
        if len(flights) > 1:
            print('Add action for more than one flight on that day with same flight no')
            df = pd.DataFrame(flights) # this will return a df with multiple rows
            return
        if len(flights) == 1:
            df = pd.DataFrame(flights)
            df = add_local_times(df)
            df = extract_info_from_datetime_col(df)
            X_new = clean_df(df)
            return X_new


if __name__ == '__main__':
    response = get_raw_flight_details(flight_number='DAL383', date=datetime.date(2022,12,13))
    print(process_flight_details(response))
