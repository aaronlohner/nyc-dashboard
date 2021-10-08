import pandas as pd
import os.path as osp

dir = osp.dirname(__file__)
data_path = osp.join(dir, '..', 'data', 'nyc_311_limit_2020.csv')
# the column at index 8 (i.e. the 9th column) is the "Incident Zip" column
df = pd.read_csv(data_path, usecols=[8], header=None)
print(len(df[8].unique()))