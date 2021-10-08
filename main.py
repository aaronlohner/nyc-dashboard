import pandas as pd

from bokeh.layouts import column, row
from bokeh.io import show
from bokeh.models import Div, Dropdown, ColumnDataSource
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc

#from scripts.data import monthly_avg_incident_times
from scripts.nyc_dash import load_data, clean_data, monthly_avg_incident_time

df = clean_data(load_data())
zipcodes = df['Incident Zip'].unique()
zipcodes_str = [str(zip) for zip in zipcodes]
zipcodes_dict = dict(zip(zipcodes_str, zipcodes))

monthly_avg_incident_times = [monthly_avg_incident_time(df, m) for m in range(12)]
monthly_avg_incident_times_z1 = [monthly_avg_incident_time(df, m, zipcodes[0]) for m in range(12)]
monthly_avg_incident_times_z2 = [monthly_avg_incident_time(df, m, zipcodes[1]) for m in range(12)]

dropdown_z1 = Dropdown(label="Zipcode 1", button_type="primary", menu=zipcodes_str) #Enumeration(default, primary, success, warning, danger, light)
dropdown_z2 = Dropdown(label="Zipcode 2", button_type="warning", menu=zipcodes_str)

text_z1 = Div(text=f"<p>Zipcode 1: {zipcodes[0]}</p>""", width=300, height=30,)
text_z2 = Div(text=f"<p>Zipcode 2: {zipcodes[1]}</p>""", width=300, height=30,)

# create a plot and style its properties
p = figure(toolbar_location=None, title='Monthly average incident create-to-close time', x_axis_type='datetime',
        x_axis_label='Month', y_axis_label='Average incident create-to-closed time (hours)')

months = pd.date_range('2020-01-01','2020-12-31', freq='MS').tolist()

data={'Month' : months,
        'All' : monthly_avg_incident_times,
        'z1' : monthly_avg_incident_times_z1,
        'z2' : monthly_avg_incident_times_z2}
source = ColumnDataSource(data=data)

# p.line(months, monthly_avg_incident_times, line_color="blue", legend_label="All")
# p.line(months, monthly_avg_incident_times_z1, line_color="red", legend_label=f"Zip: {zipcodes[1]}")
# p.line(months, monthly_avg_incident_times_z2, line_color="green", legend_label=f"Zip: {zipcodes[2]}")
p.line('Month', 'All', source=source, line_color="blue", legend_label="All")
p.line('Month', 'z1', source=source, line_color="red", legend_label=text_z1.text)
p.line('Month', 'z2', source=source, line_color="green", legend_label=text_z2.text)

def update_zipcode1(event):
        source.data['z1'] = [monthly_avg_incident_time(df, m, zipcodes_dict[event.item]) for m in range(12)]
        #source.data = new_data
        text_z1.text = "Zipcode 1: " + event.item

def update_zipcode2(event):
        source.data['z2'] = [monthly_avg_incident_time(df, m, zipcodes_dict[event.item]) for m in range(12)]
        text_z2.text = "Zipcode 2: " + event.item

dropdown_z1.on_click(update_zipcode1)
dropdown_z2.on_click(update_zipcode2)

#curdoc().add_root(row(p, column(row(dropdown_z1, dropdown_z2), row(text_z1, text_z2))))
curdoc().add_root(column(dropdown_z1, dropdown_z2, p))