import os.path as osp
import pandas as pd
import json
from bokeh.layouts import column
from bokeh.models import Div, Dropdown, ColumnDataSource
from bokeh.plotting import figure, curdoc

# Load zipcode data
dirname = osp.dirname(__file__)
data_path = osp.join(dirname, 'zipcodes.json')
zipcodes = json.load(open(data_path,))
zipcodes_menu = list(zipcodes.keys())[1:] # exclude 'all' (the first key) from dropdown menus
zipcodes_menu.sort()
zip1_default = zipcodes_menu[0]
zip2_default = zipcodes_menu[1]

# Widgets
dropdown_z1 = Dropdown(label="Zipcode 1", button_type="primary", menu=zipcodes_menu)
dropdown_z2 = Dropdown(label="Zipcode 2", button_type="warning", menu=zipcodes_menu)
text_z1 = Div(text=f"<p>Zipcode 1: {zip1_default}</p>""", width=300, height=30,)
text_z2 = Div(text=f"<p>Zipcode 2: {zip2_default}</p>""", width=300, height=30,)
text_login = Div(text=f"<p>Please enter the correct username and password as parameters in the URL to login.</p>""",)

# Build plot
p = figure(toolbar_location=None, title='Monthly average incident create-to-close time', x_axis_type='datetime',
        x_axis_label='Month', y_axis_label='Average incident create-to-closed time (hours)')

# Build plot data
months = pd.date_range('2020-01-01','2020-12-31', freq='MS').tolist()
data={'Month' : months,
        'All' : zipcodes['all'],
        'z1' : zipcodes[zip1_default],
        'z2' : zipcodes[zip2_default]}
source = ColumnDataSource(data=data)

# Plot the data
p.line('Month', 'All', source=source, line_color="red", legend_label="All zipcodes")
p.line('Month', 'z1', source=source, line_color="blue", legend_label="Zipcode 1")
p.line('Month', 'z2', source=source, line_color="orange", legend_label="Zipcode 2")

# Callbacks
def update_zipcode1(event):
        source.data['z1'] = zipcodes[event.item]
        text_z1.text = "Zipcode 1: " + event.item

def update_zipcode2(event):
        source.data['z2'] = zipcodes[event.item]
        text_z2.text = "Zipcode 2: " + event.item
        
dropdown_z1.on_click(update_zipcode1)
dropdown_z2.on_click(update_zipcode2)

url = curdoc().session_context.request.arguments
if (len(url) == 2 and 'username' in url.keys() and 'password' in url.keys() and 
        url['username'][0].decode('utf-8') == 'nyc' and url['password'][0].decode('utf-8') == 'iheartnyc'):
        curdoc().add_root(column(dropdown_z1, text_z1, dropdown_z2, text_z2, p))
else:
        curdoc().add_root(text_login)