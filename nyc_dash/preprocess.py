from numpy.core.fromnumeric import mean
import pandas as pd
import os.path as osp
from pandas._libs.tslibs.timedeltas import Timedelta
import json

def load_data(datafile:str, headerfile:str) -> pd.DataFrame:
    dirname = osp.dirname(__file__)
    data_path = osp.join(dirname, datafile)
    header_path = osp.join(dirname, headerfile)
    header = [line.rstrip() for line in open(header_path)]
    return pd.read_csv(data_path, usecols=['Created Date', 'Closed Date', 'Incident Zip'], names=header)#, nrows=1_000)

def clean_data(df:pd.DataFrame) -> pd.DataFrame:
    # Drop NAs (zipcodes, closed dates)
    df.dropna(inplace=True, subset=['Closed Date', 'Incident Zip'])
    df['Incident Zip'] = pd.to_numeric(df['Incident Zip'], downcast='integer') #NEEDED?

    # Remove negative time differences
    df[['Created Date', 'Closed Date']] = df[['Created Date', 'Closed Date']].apply(pd.to_datetime)
    df = df[df[['Created Date', 'Closed Date']].apply(lambda x : x[1] - x[0] > pd.Timedelta(0), axis=1)]
    return df

def monthly_avg_incident_time(df:pd.DataFrame, month_num:int, zip:int=None) -> float:
    df = df[df['Created Date'].dt.month == month_num]
    if zip is not None:
        df = df[df['Incident Zip'] == zip]
    if df.shape[0] == 0:
        return 0 # TEMPORARY MEASURE
    diff = df[['Created Date', 'Closed Date']].apply(lambda x : pd.Timedelta(x[1] - x[0]), axis=1)
    return float(mean(diff).seconds/3600)

def monthly_avg_incident_times(df:pd.DataFrame, zip:int=None):
    return [monthly_avg_incident_time(df, m, zip) for m in range(1, 13)]


def write_json_output(df:pd.DataFrame, out:str):
    zipcodes = df['Incident Zip'].unique()
    #zipcodes.sort()
    json_dict = {}
    json_dict["all"] = monthly_avg_incident_times(df)
    for zip in zipcodes:
        json_dict[str(zip)] = monthly_avg_incident_times(df, zip)

    json_obj = json.dumps(json_dict, indent = 4)
    with open(out, "w") as output:
        output.write(json_obj)

if __name__ == '__main__':
    df = clean_data(load_data('nyc_311_limit_2020.csv', 'header.txt'))
    #write_json_output(df, 'zipcodes.json')