# -*- coding: utf-8 -*-
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
import dash_auth
from config import VALID_USERNAME_PASSWORD_PAIRS
from data_manager import SimpleDataManager as DataManager
from flask import Flask, send_from_directory
from views import get_global_stat_view, get_head_view

# from data_manager import DataManager
import pandas as pd


data_manager = DataManager()

server = Flask(__name__)
app = dash.Dash(server=server)
auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

DOWNLOAD_DIRECTORY = "data"


@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(DOWNLOAD_DIRECTORY, path, as_attachment=True)


app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("Data Quality", className="six columns"),
                html.A(
                    "Download data",
                    id="download-link",
                    className="six columns",
                    style={"textAlign": "right"},
                ),
            ],
            className="row flex-display",
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
                        "height": "60px",
                        "lineHeight": "60px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                    },
                    className="six columns",
                ),
                dcc.Upload(
                    id="upload-data-overwrite",
                    children=html.Div(
                        html.A(
                            [
                                "Select a CSV or a XLS* file to",
                                html.Strong(" OVERWRITE "),
                                "current data",
                            ]
                        )
                    ),
                    style={
                        "height": "60px",
                        "lineHeight": "60px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                    },
                    className="six columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Hr(className="custom-hr"),
        # Stat on dataset
        dcc.Loading(
            [
                html.H3("Dataset informations :"),
                html.Div(id="dataset_stat"),
                html.Hr(className="custom-hr"),
                html.Div(id="output-data-upload"),
            ]
        ),
        html.Hr(className="custom-hr"),
        # Generate pandas profiling report
        html.Div(
            0, id="generate_profiling_button_last_ts_click", style={"display": "none"}
        ),
        html.Div(
            [
                html.Button(
                    "Generate Profiling Report",
                    id="generate-profiling-button",
                    className="six columns",
                ),
                dcc.Loading(
                    [
                        html.A(
                            "Download Profiling Report",
                            id="download-profiling-report-link",
                            style={"display": "none", "textAlign": "right"},
                        )
                    ],
                    className="six columns",
                ),
            ],
            className="row flex-display",
        ),
    ]
)


# Table - dataset's head
@app.callback(
    [Output("output-data-upload", "children"), Output("download-link", "href")],
    [Input("upload-data-add", "contents"), Input("upload-data-overwrite", "contents")],
    [State("upload-data-add", "filename"), State("upload-data-overwrite", "filename")],
)
def update_output_data_upload(
    content_add, content_overwrite, filename_add, filename_overwrite
):
    if content_add is not None:
        data_manager.process_file(content_add, filename_add, overwrite=False)
    elif content_overwrite is not None:
        data_manager.process_file(content_overwrite, filename_overwrite, overwrite=True)

    download_data = data_manager.data.to_csv(index=False, encoding="utf-8")
    download_data = "data:text/csv;charset=utf-8," + urllib.parse.quote(download_data)

    return get_head_view(data_manager.data), download_data


# Stat on the global dataset
@app.callback(
    Output("dataset_stat", "children"), [Input("output-data-upload", "children")]
)
def display_df_stat(content):
    return get_global_stat_view(data_manager.data)


global generate_profiling_button_last_ts_click
generate_profiling_button_last_ts_click = 0


@app.callback(
    [
        Output("download-profiling-report-link", "href"),
        Output("download-profiling-report-link", "style"),
        Output("generate_profiling_button_last_ts_click", "children"),
    ],
    [
        Input("generate-profiling-button", "n_clicks_timestamp"),
        Input("upload-data-add", "last_modified"),
        Input("upload-data-overwrite", "last_modified"),
    ],
    [State("generate_profiling_button_last_ts_click", "children")],
)
def generate_profilin_report(ts_click, ts_add, ts_overwrite, last_ts_click):
    last_ts_click = int(last_ts_click)
    if ts_click is None:
        return "", {"display": "none"}, 0
    if ts_click > last_ts_click:
        profile = data_manager.generate_profiling_report()
        return (
            "/download/profiling-report.html",
            {"display": "block", "textAlign": "right"},
            ts_click,
        )

    return "", {"display": "none"}, 0


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
