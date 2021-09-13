# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from os.path import getmtime

import dash
from dash import dcc, Output, Input, State, ALL
from dash import html

import plotly.express as px

import pandas as pd

from stats_getter import StatsGetter

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Update Dashboard every n seconds
interval_duration = 1
# Stats file path
stats_file = '../MultiStreamUnsupervisedFaceIdentification/Dump/dunya/Stats/stats.pkl'
# Stats Object
stats_obj = StatsGetter(stats_file)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                assets_folder='../MultiStreamUnsupervisedFaceIdentification/Dump/dunya/', assets_url_path='/')

main_graph_init_fig = px.bar(
    pd.DataFrame(
        stats_obj.get_frequent_persons(n=100, id_only=False),
        columns=['Person-ID', 'Occurrences']
    ),
    x='Person-ID',
    y='Occurrences',
)

main_graph_init_fig.update_xaxes(type='category')

small_graph_init_fig = px.bar(
    pd.DataFrame(
        stats_obj.get_time_frequency_of_id(0),
        columns=['Time-Stamp', 'Occurrences']
    ),
    x='Time-Stamp',
    y='Occurrences',
    title='Graph of ID: ' + str(0)
)

app.layout = html.Div(children=[
    html.H1(children='Live Stream Video Analytics'),

    html.Div(children='''
        Dashboard for Analysis on TV Stream.
    '''),
    html.Div(children=[
    html.H3(children='Recent Faces'),
    html.Div(id='recent_faces'),

    html.H3(children='Frequent Faces'),
    html.Div(id='frequent_faces')
    ], style={'display': 'inline-block', 'width': '40%'}),
    html.Div(children=[
        dcc.Graph(id='small_graph', figure=small_graph_init_fig)
    ], style={'display': 'inline-block'}),

    dcc.Graph(id='large_graph', figure=main_graph_init_fig),


    dcc.Interval(id='interval_component',
                 interval=interval_duration * 1000,  # in milliseconds,
                 n_intervals=0),
    dcc.Store(id='file_update_time', data=getmtime(stats_file))
])


@app.callback(Output('file_update_time', 'data'), Input('interval_component', 'n_intervals'))
def check_file_for_update(n):
    stats_obj.update_data()
    return ('mtime', getmtime(stats_file))


@app.callback(Output('recent_faces', 'children'), Input('file_update_time', 'data'))
def update_recent_faces(data):
    return [html.Img(src=f'Faces/{i}/0.png',
                     id={'type': 'face_img', 'index': str(i)})
            for i in stats_obj.get_recent_persons()]


@app.callback(Output('frequent_faces', 'children'), Input('file_update_time', 'data'))
def update_frequent_faces(data):
    return [html.Img(src=f'Faces/{i}/0.png',
                     id={'type': 'face_img', 'index': str(i)})
            for i in stats_obj.get_frequent_persons()]


@app.callback(Output('large_graph', 'figure'), Input('file_update_time', 'data'))
def update_large_graph(data):
    return_figure = px.bar(
        pd.DataFrame(
            stats_obj.get_frequent_persons(n=100, id_only=False),
            columns=['Person-ID', 'Occurrences']
        ),
        x='Person-ID',
        y='Occurrences',
    )
    return_figure.update_xaxes(type='category')

    return return_figure


@app.callback(Output('small_graph', 'figure'),
              Input({'type': 'face_img', 'index': ALL}, 'n_clicks'),
              State({'type': 'face_img', 'index': ALL}, 'id'))
def update_small_graph(n_clicks, element_id):
    # Loop and find index of clicked element
    is_clicked = False
    for i in range(len(n_clicks)):
        if n_clicks[i] is not None:
            is_clicked = True
            break
    if is_clicked:
        person_id = element_id[i]['index']
        return_figure = px.bar(
            pd.DataFrame(
                stats_obj.get_time_frequency_of_id(int(person_id)),
                columns=['Time-Stamp', 'Occurrences']
            ),
            x='Time-Stamp',
            y='Occurrences',
            title='Graph of ID: ' + person_id
        )
        return return_figure
    return dash.no_update






if __name__ == '__main__':
    app.run_server(debug=True)
