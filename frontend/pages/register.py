import requests
from dash import html, Input, State, Output
import dash_mantine_components as dmc
from dash_iconify import DashIconify


AUTH_URL = "http://localhost:5000/auth"


def register_page():
    return html.Div([
        html.Div(id="register-notifications-container"),

        dmc.Stack(children=[
            dmc.TextInput(label="User Name", w=200, required=True, id="username"),
            dmc.PasswordInput(label="Password", w=200, required=True, id="password"),
            dmc.Button("Register", variant="filled", leftSection=DashIconify(icon="lets-icons:user-add"),
                       id="register-btn")
        ], align="center", justify="center")
    ])


def register_callback_register(app):
    @app.callback(
        Output("register-notifications-container", "children"),
        Input("register-btn", "n_clicks"),
        State("username", "value"),
        State("password", "value"),
        prevent_initial_call=True,
    )
    def register(n_clicks, username, password):
        if n_clicks:
            if username and password:
                response = requests.post(f"{AUTH_URL}/register",
                                         json={"username": username, "password": password})
                if response.status_code == 200:
                    return dmc.Notification(
                        title="Register success.", action="show", message="Welcome!",
                        icon=DashIconify(icon="ic:round-celebration"),
                    )
                else:
                    msg = response.json()["msg"]
                    return dmc.Notification(
                        title="Register Failed.", action="show", message=msg,
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