import requests
from dash import html, Input, State, Output, no_update
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from flask import session

AUTH_URL = "http://localhost:5000/auth"


# TODO check LoadingOverlay component

def login_page():
    return html.Div([
        html.Div(id="login-notifications-container"),

        dmc.Stack([
            dmc.Flex([
                dmc.Stack(children=[
                    dmc.TextInput(label="User Name", w=200, required=True, id="username"),
                    dmc.PasswordInput(label="Password", w=200, required=True, id="password"),
                ], align="center", justify="center"),
                dmc.Button("Reset Pwd", variant="subtle", id="reset-pwd"),
            ], direction="row", align="flex-end", justify="center", gap="lg"),

            dmc.Divider(),
            dmc.Button("Login", variant="filled", leftSection=DashIconify(icon="lets-icons:user-alt"),
                       id="login-btn")
        ], align="center", justify="center")

    ])


def register_callback_login(app):
    @app.callback(
        Output("login-notifications-container", "children"),
        Input("login-btn", "n_clicks"),
        State("username", "value"),
        State("password", "value"),
        prevent_initial_call=True,
    )
    def login(n_clicks, username, password):
        if n_clicks:
            if username and password:
                response = requests.post(f"{AUTH_URL}/login",
                                         json={"username": username, "password": password})
                if response.status_code == 200:
                    session["username"] = username
                    session["access_token"] = response.json().get("access_token")
                    session["refresh_token"] = response.json().get("refresh_token")
                    return dmc.Notification(
                        title="Login success.", action="show", message="Welcome!",
                        icon=DashIconify(icon="ic:round-celebration"),
                    )
                else:
                    msg = response.json()["msg"]
                    return dmc.Notification(
                        title="Login Failed.", action="show", message=msg,
                        icon=DashIconify(icon="icon-park-solid:error"), autoClose=2000, color="red",
                    )
            else:
                missing_field = []
                if not username:
                    missing_field.append("Username")
                if not password:
                    missing_field.append("Password")
                return dmc.Notification(
                    title="Error", action="show", message=f"MISSING: {', '.join(missing_field)}",
                    icon=DashIconify(icon="icon-park-solid:error"), autoClose=2000, color="red",
                )

    @app.callback(
        Output('url', 'href'),
        Input("reset-pwd", "n_clicks"),
        State("username", "value"),
        prevent_initial_call=True,
    )
    def reset_pwd(n_clicks, username):
        if n_clicks:
            return f'/resetpwd?username={username}'
        return no_update
