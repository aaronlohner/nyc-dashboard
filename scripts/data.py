from scripts.nyc_dash import clean_data, load_data, monthly_avg_incident_time

df = clean_data(load_data())
zipcodes = df['Incident Zip'].unique()
monthly_avg_incident_times = [monthly_avg_incident_time(df, m) for m in range(1,13)]

# import pandas as pd
# from datetime import datetime
# months = pd.date_range('2020-01-01','2020-12-31', freq='MS').tolist()
# print(months[1])