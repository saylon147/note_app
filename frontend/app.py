from dash import Dash, html, Input, Output, State, callback, ctx
import dash_bootstrap_components as dbc
import requests

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
           suppress_callback_exceptions=True)

API_URL = "http://localhost:5000/api"

app.layout = dbc.Container([
    html.Br(),
    dbc.Nav([
        dbc.NavItem(dbc.NavLink("Login", id="login-tab", active=True, href="#")),
        dbc.NavItem(dbc.NavLink("Register", id="register-tab", href="#")),
        dbc.NavItem(dbc.NavLink("Notes", id="notes-tab", disabled=True, href="#"))
    ], pills=True),
    html.Br(),
    html.Div(id='tab-content')
])


def login_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.FormFloating([
                    dbc.Input(type="text", id="login-username", maxlength=16),
                    dbc.Label("Username"),
                ], className="mb-2"),
                dbc.FormFloating([
                    dbc.Input(type="password", id="login-password", maxlength=8),
                    dbc.Label("Password"),
                ], className="mb-2"),
            ], width=6),
            dbc.Col([
                dbc.Button("Login", id="login-button", outline=True,
                           color="primary", className="me-1")
            ])
        ], justify="center"),
        html.Div(id="login-output", className="mt-2", style={
            # "width": "80%",
            "word-wrap": "break-word",
        })
    ])


def register_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.FormFloating([
                    dbc.Input(type="text", id="register-username", maxlength=16),
                    dbc.Label("Username (maxlength=16)"),
                ], className="mb-2"),
                dbc.FormFloating([
                    dbc.Input(type="password", id="register-password", maxlength=8),
                    dbc.Label("Password (maxlength=8)"),
                ], className="mb-2"),
            ], width=6),
            dbc.Col([
                dbc.Button("Register", id="register-button", outline=True,
                           color="success", className="me-1")
            ])
        ], justify="center"),
        html.Div(id="register-output", className="mt-2", style={
            # "width": "80%",
            "word-wrap": "break-word",
        })
    ])


def notes_layout():
    return dbc.Container([

    ])


@callback(
    Output("tab-content", "children"),
    Output("login-tab", "active"),
    Output("register-tab", "active"),
    Output("notes-tab", "active"),
    Input("login-tab", "n_clicks"),
    Input("register-tab", "n_clicks"),
    Input("notes-tab", "n_clicks")
)
def render_tab_content(n_clicks_login, n_clicks_register, n_clicks_notes):
    if not ctx.triggered:
        return login_layout(), True, False, False

    if ctx.triggered_id == "login-tab":
        return login_layout(), True, False, False
    elif ctx.triggered_id == "register-tab":
        return register_layout(), False, True, False
    elif ctx.triggered_id == "notes-tab":
        return notes_layout(), False, False, True
    else:
        return html.Div("404 - Page not found"), False, False, False


@callback(
    Output("login-output", "children"),
    Output("notes-tab", "disabled"),
    Input("login-button", "n_clicks"),
    State("login-username", "value"),
    State("login-password", "value")
)
def login(n_clicks, username, password):
    if n_clicks:
        response = requests.post(f"{API_URL}/auth/login", json={"username": username, "password": password})
        if response.status_code == 200:
            # token = response.json()["access_token"]
            return "Login successful.", False
        else:
            return "Login failed.", True
    return "", True


@callback(
    Output("register-output", "children"),
    Input("register-button", "n_clicks"),
    State("register-username", "value"),
    State("register-password", "value")
)
def register(n_clicks, username, password):
    if n_clicks:
        response = requests.post(f"{API_URL}/auth/register", json={"username": username, "password": password})
        if response.status_code == 201:
            return "Registration successful."
        else:
            return "Registration failed."
    return ""


if __name__ == '__main__':
    app.run(debug=True)
