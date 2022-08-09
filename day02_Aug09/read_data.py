# This function reads the data from GAMIT timeseries files. This function is called in reading_GPS_files jupyter notebook to read the files.
import pandas as pd
import numpy as np
import datetime

def read_data(name_of_file):
    header_length=36 # a constant for this file type
    data = pd.read_csv(name_of_file,skiprows=header_length,delim_whitespace=True)
    # edit the 2nd column to be decimal year instead of a constant time of 1159.
    decyr=get_decimal_year(data['*YYYYMMDD'])
    data = data.drop(columns='HHMMSS')
    data.insert(1,'DecYr',decyr)
    return data
    
def get_decimal_year(dates):
    decyr=[]
    for i in range(len(dates)):
        day=str(dates[i])
        dt=datetime.date(int(day[0:4]),int(day[4:6]),int(day[6:]))
        decyr.append(year_fraction(dt))
    return decyr

def year_fraction(date):
    # special: convert the day/time to a decimal year
    start = datetime.date(date.year, 1, 1).toordinal()
    year_length = datetime.date(date.year+1, 1, 1).toordinal() - start
    # add 0.5 to have centered days
    return date.year + float(date.toordinal() - start + 0.4993) / year_length

