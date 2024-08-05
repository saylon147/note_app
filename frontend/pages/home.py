from dash import html, dcc
import dash_mantine_components as dmc
from flask import session


def get_username():
    if session:
        return f"username: {session["username"]}"
    else:
        return "no user"


def get_access_token():
    if session:
        return f"access token: {session["access_token"]}"
    else:
        return "no session"


def home_page():
    return html.Div([
        html.H1("Home Page"),
        dmc.Container(children=[
            dmc.Text(get_username()),
            dmc.Text(get_access_token(), style={"wordWrap": "break-word", "whiteSpace": "normal"})
        ]),
    ])
