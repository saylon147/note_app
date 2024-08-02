import requests
from dash import html, Input, State, Output
import dash_mantine_components as dmc
from dash_iconify import DashIconify

AUTH_URL = "http://localhost:5000/auth"


def reset_pwd_page(username):
    return html.Div([
        html.Div(id="reset-pwd-notifications-container"),

        dmc.Stack([
            dmc.TextInput(label="User Name", w=200, disabled=True, id="username", value=username),
            dmc.PasswordInput(label="Password", w=200, required=True, id="password"),
            dmc.Button("Reset Password", variant="filled", leftSection=DashIconify(icon="carbon:password"),
                       id="reset-pwd-btn")
        ], align="center", justify="center")
    ])


def register_callback_reset_pwd(app):
    @app.callback(
        Output("reset-pwd-notifications-container", "children"),
        Input("reset-pwd-btn", "n_clicks"),
        State("username", "value"),
        State("password", "value")
    )
    def reset_password(n_clicks, username, password):
        if n_clicks:
            if password:
                response = requests.post(f"{AUTH_URL}/resetpwd",
                                         json={"username": username, "password": password})
                if response.status_code == 200:
                    return dmc.Notification(
                        title="Reset password success.", action="show", message="",
                        icon=DashIconify(icon="ic:round-celebration"),
                    )
                else:
                    msg = response.json()["msg"]
                    return dmc.Notification(
                        title="Reset password Failed.", action="show", message=msg,
                        icon=DashIconify(icon="icon-park-solid:error"), autoClose=2000, color="red",
                    )
            else:
                return dmc.Notification(
                    title="Error", action="show", message=f"MISSING: Password",
                    icon=DashIconify(icon="icon-park-solid:error"), autoClose=2000, color="red",
                )
