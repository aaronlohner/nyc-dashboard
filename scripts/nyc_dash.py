from numpy.core.fromnumeric import mean, shape
import pandas as pd
import os.path as osp
from pandas._libs.tslibs.timedeltas import Timedelta
from datetime import datetime

def load_data() -> pd.DataFrame:
    dir = osp.dirname(__file__)
    data_path = osp.join(dir, '..', 'data', 'nyc_311_limit_2020.csv')
    header_path = osp.join(dir, '..', 'data', 'header.txt')
    header = [line.rstrip() for line in open(header_path)]
    return pd.read_csv(data_path, usecols=['Unique Key', 'Created Date', 'Closed Date', 'Incident Zip'], names=header, nrows=1_000)

def clean_data(df:pd.DataFrame) -> pd.DataFrame:
    # Drop NAs (zipcodes, closed dates)
    df.dropna(inplace=True, subset=['Closed Date', 'Incident Zip'])
    df['Incident Zip'] = pd.to_numeric(df['Incident Zip'], downcast='integer') #NEEDED?

    # Remove negative time differences
    df[['Created Date', 'Closed Date']] = df[['Created Date', 'Closed Date']].apply(pd.to_datetime)
    df = df[df[['Created Date', 'Closed Date']].apply(lambda x : x[1] - x[0] > pd.Timedelta(0), axis=1)]
    return df

def monthly_avg_incident_time(df:pd.DataFrame, month_num:int, zip:int=None) -> int:
    df = df[df['Created Date'].dt.month == month_num]
    if zip is not None:
        df = df[df['Incident Zip'] == zip]
    if df.shape[0] == 0:
        return 0 # TEMPORARY MEASURE
    diff = df[['Created Date', 'Closed Date']].apply(lambda x : pd.Timedelta(x[1] - x[0]), axis=1)
    return mean(diff).seconds/3600


if __name__ == '__main__':
    df = clean_data(load_data())
    #print(df)
    #print(monthly_avg_incident_time(df, 7))
    print(monthly_avg_incident_time(df, 7, 11210))