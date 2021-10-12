import os.path as osp
import pandas as pd
from numpy.core.fromnumeric import mean
import json

dirname = osp.dirname(__file__)

def load_data(datafile:str, headerfile:str) -> pd.DataFrame:
    data_path = osp.join(dirname, '..', 'data', datafile)
    header_path = osp.join(dirname, headerfile)
    header = [line.rstrip() for line in open(header_path)]
    return pd.read_csv(data_path, usecols=['Created Date', 'Closed Date', 'Incident Zip'], names=header,
                        dtype={'Incident Zip':'str'}, parse_dates=['Created Date', 'Closed Date'], nrows=100)

def clean_data(df:pd.DataFrame) -> pd.DataFrame:
    # Drop NAs (zipcodes, closed dates)
    df.dropna(inplace=True, subset=['Closed Date', 'Incident Zip'])
    # Remove negative time differences
    df = df[df[['Created Date', 'Closed Date']].apply(lambda x : x[1] - x[0] > pd.Timedelta(0), axis=1)]
    return df

def monthly_avg_incident_time(df:pd.DataFrame, month_num:int, zip:str=None) -> float:
    df = df[df['Closed Date'].dt.month == month_num]
    if zip is not None: # only None when looking at all zipcodes
        df = df[df['Incident Zip'] == zip]
    if df.shape[0] == 0: # if no incidents resolved in a month, set avg resolve time to 0
        return 0
    diff = df[['Created Date', 'Closed Date']].apply(lambda x : pd.Timedelta(x[1] - x[0]), axis=1)
    return float(mean(diff).seconds/3600)

def monthly_avg_incident_times(df:pd.DataFrame, zip:str=None):
    return [monthly_avg_incident_time(df, m, zip) for m in range(1, 13)]


def write_json_output(df:pd.DataFrame, out:str):
    zipcodes = df['Incident Zip'].unique()
    json_dict = {}
    json_dict["all"] = monthly_avg_incident_times(df)
    for zip in zipcodes:
        json_dict[zip] = monthly_avg_incident_times(df, zip)

    json_obj = json.dumps(json_dict, indent = 4)
    with open(out, "w") as output:
        output.write(json_obj)


if __name__ == '__main__':
    df = clean_data(load_data('nyc_311_limit_trimmed.csv', 'header.txt'))
    #write_json_output(df, osp.join(dirname, 'zipcodes.json'))
    diff = df[['Created Date', 'Closed Date']].apply(lambda x : pd.Timedelta(x[1] - x[0]), axis=1)
    s = 0
    for d in diff:
        print(d)
        s = s + d.seconds
    #print(diff.shape[0])
    print(s)
    print(s/diff.shape[0])
    print(mean(diff).seconds)
    