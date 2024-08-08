import requests
from dash import html, Input, State, Output, dcc, no_update
import dash_mantine_components as dmc
from dash_iconify import DashIconify


def upload_page():
    return html.Div([
        html.Div(id="upload-notifications-container"),
        dcc.Store(id='stored-file-content'),

        dcc.Upload(
            id='upload-file',
            children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
            style={
                'width': '100%', 'height': '60px', 'lineHeight': '60px',
                'borderWidth': '1px', 'borderStyle': 'dashed',
                'borderRadius': '5px', 'textAlign': 'center'
            },
            multiple=False
        ),
        html.Br(),
        dmc.Stack(children=[
            dmc.Text("文件名", id='upload-filename'),
            dmc.Button("Upload", variant="filled",
                       leftSection=DashIconify(icon="ant-design:cloud-upload-outlined"),
                       id="upload-btn")
        ], align="flex-start"),

    ])


def register_callback_upload(app):
    @app.callback(
        Output("upload-filename", "children"),
        Output("stored-file-content", "data"),
        Input("upload-file", "contents"),
        State("upload-file", "filename"),
        prevent_initial_call=True,
    )
    def select_file(contents, filename):
        if contents is not None:
            return filename, contents
        return no_update, None

    @app.callback(
        Output("upload-notifications-container", "children"),
        Input("upload-btn", "n_clicks"),
        State('stored-file-content', 'data'),
        prevent_initial_call=True,
    )
    def upload_file(n_clicks, contents):
        print(contents)
        if n_clicks and contents is not None:
            return dmc.Notification(
                title="Upload success.", action="show", message="Welcome!",
                icon=DashIconify(icon="ic:round-celebration"),
            )
        return no_update
