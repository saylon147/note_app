from dash import Dash, html, Input, Output, State, callback, ctx, dcc
import dash_bootstrap_components as dbc
import requests

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
           suppress_callback_exceptions=True)

API_URL = "http://localhost:5000/api"

show_style = {}
hide_style = {'display': 'none'}


def login_register_page(is_register=False):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.FormFloating([
                    dbc.Input(type="text", id="username", maxlength=16),
                    dbc.Label("Username"),
                ], className="mb-2"),
                dbc.FormFloating([
                    dbc.Input(type="password", id="password", maxlength=8),
                    dbc.Label("Password"),
                ], className="mb-2"),
            ], width=6),
            dbc.Col([
                dbc.Button("Login", id="login-button", outline=True,
                           style=show_style if not is_register else hide_style,
                           color="primary", className="me-1"),
                dbc.Button("Register", id="register-button", outline=True,
                           style=hide_style if not is_register else show_style,
                           color="primary", className="me-1")
            ])
        ], justify="center"),
        html.Div(id="login-output", className="mt-2", style={
            # "width": "80%",
            "word-wrap": "break-word",
        })
    ])


app.layout = dbc.Container([
    dcc.Store(id='login-state', storage_type='local'),  # 存储登录状态
    dcc.Location(id='url', refresh=False),
    html.Br(),
    dbc.Nav([
        dbc.NavItem(dbc.NavLink("Login", id="login-link", active=True, href="/login", style=show_style)),
        dbc.NavItem(dbc.NavLink("Register", id="register-link", href="/register", style=show_style)),
        dbc.NavItem(dbc.NavLink("Notes", id="notes-link", href="/notes", style=hide_style)),
        dbc.NavItem(dbc.NavLink("Logout", id="logout-link", href="/logout", style=hide_style))
    ], pills=True),
    html.Br(),
    html.Div(id='link-content', children=login_register_page())
])


def notes_page():
    return dbc.Container([
        html.H1("Notes Page")
    ])


@callback([Output("link-content", "children"),
           Output("login-link", "active"),
           Output("register-link", "active"),
           Output("notes-link", "active"),
           Output("login-link", "style"),
           Output("register-link", "style"),
           Output("notes-link", "style"),
           Output("logout-link", "style"),
           Output("login-state", "data")],
          [Input("url", "pathname"),
           Input("login-button", "n_clicks"),
           Input("register-button", "n_clicks")],
          [State("username", "value"),
           State("password", "value"),
           State("login-state", "data")],
          prevent_initial_call=True
          )
def display_page(pathname, login_click, register_click,
                 username, password, login_state):
    print(pathname)
    if pathname == '/login' or pathname == '/':
        if username == "" and password == "":
            return (login_register_page(), True, False, False,
                    show_style, show_style, hide_style, hide_style, login_state)
    elif pathname == "/register":
        return (login_register_page(True), False, True, False,
                show_style, show_style, hide_style, hide_style, login_state)
    elif pathname == "/notes" and login_state:
        return (notes_page(), False, False, True,
                hide_style, hide_style, show_style, show_style, login_state)
    elif pathname == "/logout" and login_state:
        # do logout
        return (login_register_page(), True, False, False,
                show_style, show_style, hide_style, hide_style, False)

    if login_click:
        print("do login")
        response = requests.post(f"{API_URL}/auth/login", json={"username": username, "password": password})
        if response.status_code == 200:
            print("login success")
            # token = response.json()["access_token"]
            return (notes_page(), False, False, True,
                    hide_style, hide_style, show_style, show_style, True)
        else:
            print("login failed")
            return (login_register_page(), True, False, False,
                    show_style, show_style, hide_style, hide_style, login_state)

    if register_click:
        print("do register")
        response = requests.post(f"{API_URL}/auth/register", json={"username": username, "password": password})
        if response.status_code == 201:
            return (notes_page(), False, False, True,
                    hide_style, hide_style, show_style, show_style, True)
        else:
            return (login_register_page(True), False, True, False,
                    show_style, show_style, hide_style, hide_style, login_state)

    print("default return", username, password)
    return (login_register_page(), True, False, False,
            show_style, show_style, hide_style, hide_style, login_state)


if __name__ == '__main__':
    app.run(debug=True)
