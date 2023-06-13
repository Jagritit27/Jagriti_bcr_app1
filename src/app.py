# -*- coding: utf-8 -*-
"""
Created on Wed May 31 13:33:31 2023

@author: s5119521
"""

import glob
import dash
import random
import base64
import pandas as pd
import os
import pandas as pd
import dash_bootstrap_components as dbc
import json
import plotly.express as px
from pathlib import Path
from PIL import Image
import io
from io import BytesIO
from IPython.display import HTML
from dash import Dash, dcc, html, Input, Output, dash_table
from dash.exceptions import PreventUpdate

df = pd.read_csv('https://github.com/Jagritit27/bcr_app1/blob/main/HalveSediment_20M-Summary12.csv')


dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])
server = app.server
app.layout = html.Div([
        html.Div([
        dcc.Graph(id='graph_scatter',figure={},className="mb-4", style={'display': 'inline-block','height': '700px', 'width': '1000px'}),
        html.Div(id='hover-data')], style={'display': 'flex'}),
html.P(' Implementation Cost:'),
dcc.Slider(
                id='slider-1',
    min=df[' Implementation Cost ($)'].min(), max=df[' Implementation Cost ($)'].max(),
    value=151557545,className="dbc"),
html.P(' Dissolved Nitrogen:'),
dcc.Slider(
    id='slider-2',
    min=df[' Dissolved Nitrogen (t/yr)'].min(), max=df[' Dissolved Nitrogen (t/yr)'].max(),
    value=120,className="dbc"),
#    dcc.Slider(
#    id='slider_y',
#    min=df[' Sediment Production (t/yr)'].min(), max=df[' Sediment Production (t/yr)'].max(),
#    value=df[' Sediment Production (t/yr)'].max(),className="dbc"),
html.P(' Particulate Nitrogen (t/yr):'),
dcc.Slider(
    id='slider-3',
    min=df[' Particulate Nitrogen (t/yr)'].min(), max= df[' Particulate Nitrogen (t/yr)'].max(),
    value=204,className="dbc"),
html.P(' Opportunity Cost ($):'),
dcc.Slider(
    id='slider-4',
    min=df[' Opportunity Cost ($)'].min(), max= df[' Opportunity Cost ($)'].max(),
    value=13281671,className="dbc"),
])
    


@app.callback(
   [Output('slider-2', 'value'),
   Output('slider-3','value'),
   Output('slider-4','value')],
   Input('slider-1', 'value')
   )
#def update_slider_y(slider_x_value):
#    return 10815 * (slider_x_value ** -0.24)

def update_sliders(slider1_value):
    slider2_value = 10815 * (slider1_value ** -0.24)
    slider3_value = 372 * (slider1_value ** -0.03)
    slider4_value = 0.0145 * (slider1_value ** 1.0946)
    return slider2_value, slider3_value, slider4_value
    raise PreventUpdate
    
@app.callback(
   Output('graph_scatter', 'figure'),
   [Input('slider-1', 'value'),
   Input('slider-2', 'value'),
   Input('slider-4','value')
   ])
def update_bar_chart(slider1_value, slider2_value, slider4_value):
    slider_1 = slider1_value
    slider_2 = slider2_value
    slider_4 = slider4_value
    filtered_df = df[
        (df[' Implementation Cost ($)'] > slider_1) &
        (df[' Dissolved Nitrogen (t/yr)'] > slider_2) &
        (df[' Opportunity Cost ($)'] > slider_4)
    ]
    print(slider_1)
    dff = dict(filtered_df)

    
    # Create scatter plot
    fig = px.scatter_3d(
        dff,
        x=' Implementation Cost ($)', y=' Dissolved Nitrogen (t/yr)', 
        z=' Opportunity Cost ($)',
        hover_name = dff['Solution'])

    fig.update_traces(marker_size=50)
    fig.update_traces(marker=dict(size=3,opacity=1,
                                  line=dict(width=2,
                                            color='darkSlateGrey')),
                      selector=dict(mode='markers'),surfacecolor="LightSteelBlue")
    fig.update_layout(
    margin=dict(l=0))
    return fig
#
#@app.callback(
#    Output('hover-data', 'children'),
#    Input('graph_scatter', 'hover_data'))
#def display_hover_data(hover_data):
#    hover_data = hover_data['points'][0]['hoverdata']
#    return hover_data

if __name__ == "__main__":
    app.run_server(debug=False)
