# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 14:47:25 2019

@author: lysop
"""

import base64
import datetime
import io
import os
import urllib
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from data_manager import SimpleDataManager as DataManager
# from data_manager import DataManager
import pandas as pd


data_manager = DataManager()
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def get_global_stat_view(df):
    if df is not None:
        return html.Div(
            [
                html.P("Number of variales: {}".format(df.shape[1])),
                html.P("Number of observations: {}".format(df.shape[0])),
                html.P(
                    "Total missing values: {}%".format(
                        round(
                            100
                            * (len(df) - df.count()).sum()
                            / (df.shape[0] * df.shape[1]),
                            2,
                        )
                    )
                ),
            ]
        )
    else:
        return []


app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("Data Quality", className="six columns"),
                html.A(
                    "Download data", id="download-link",
                    className="six columns", style={"text-align": "right"}
                ),
            ],
            className="row flex-display"
        ),

        html.H3(children="Load data :"),
        html.Div(
            children=[
                dcc.Upload(
                    id="upload-data-add",
                    children=html.Div(
                        html.A(["Select a CSV or a XLS* file to add to current data"])
                    ),
                    style={
                        # "width": "100%",
                        "height": "60px",
                        "lineHeight": "60px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                        "box-sizing": "border-box",
                    },
                    className="six columns",
                ),
                dcc.Upload(
                    id="upload-data-overwrite",
                    children=html.Div(
                        html.A(["Select a CSV or a XLS* file to",
                        html.Strong(" OVERWRITE "), "current data"])
                    ),
                    style={
                        # "width": "100%",
                        "height": "60px",
                        "lineHeight": "60px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                        "box-sizing": "border-box",
                    },
                    className="six columns",
                ),
            ],
            className="row flex-display"
        ),
        # Stat on dataset
        dcc.Loading(
            [
                html.H3(id="dataset_info", children="Dataset informations:"),
                html.Div(id="dataset_stat", children=get_global_stat_view(data_manager.data)),
                html.Div(id="output-data-upload"),
            ]
        )
    ]
)


def get_head_view():
    return html.Div(
        [
            html.H5("Head :"),
            dash_table.DataTable(
                data=data_manager.data.head(10).to_dict("rows"),
                columns=[{"name": i, "id": i} for i in data_manager.data.columns],
            ),
            html.Hr(),
        ]
    )


# Table - dataset's head
@app.callback(
    [
        Output("output-data-upload", "children"),
        Output("download-link", "href")
    ],
    [
        Input("upload-data-add", "contents"),
        Input("upload-data-overwrite", "contents")
    ],
    [
        State("upload-data-add", "filename"),
        State("upload-data-overwrite", "filename")
    ]
)
def update_output_data_upload(content_add, content_overwrite, filename_add, filename_overwrite):
    if content_add is not None:
        data_manager.process_file(
            content_add, filename_add, overwrite=False
        )
    elif content_overwrite is not None:
        data_manager.process_file(
            content_overwrite, filename_overwrite, overwrite=True
        )

    download_data = data_manager.data.to_csv(index=False, encoding='utf-8')
    download_data = (
        "data:text/csv;charset=utf-8," + urllib.parse.quote(download_data)
    )

    return get_head_view(), download_data


# Stat on the global dataset
@app.callback(
    Output("dataset_stat", "children"), [Input("output-data-upload", "children")]
)
def display_df_stat(content):
    return get_global_stat_view(data_manager.data)


if __name__ == "__main__":
    app.run_server(debug=True)
