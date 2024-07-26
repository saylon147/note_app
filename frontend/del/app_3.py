from dash import Dash, html, Input, Output, State, dcc, callback_context, ALL
import dash
import dash_bootstrap_components as dbc
import requests

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
           suppress_callback_exceptions=True)

API_URL = "http://localhost:5000/api/auth"  # 添加 /auth 前缀

# 显示和隐藏样式
show_style = {}
hide_style = {'display': 'none'}

def create_navbar():
    return dbc.Nav([
        dbc.NavItem(dbc.NavLink("Login", id="login-link", href="#", n_clicks=0, style=show_style)),
        dbc.NavItem(dbc.NavLink("Register", id="register-link", href="#", n_clicks=0, style=show_style)),
        dbc.NavItem(dbc.NavLink("Notes", id="notes-link", href="#", n_clicks=0, style=hide_style)),
        dbc.NavItem(dbc.NavLink("Logout", id="logout-link", href="#", n_clicks=0, style=hide_style)),
    ], className="mb-4")

def create_login_register_form(is_register=False):
    button_text = "Register" if is_register else "Login"
    button_id = {"type": "auth-button", "index": "register"} if is_register else {"type": "auth-button", "index": "login"}
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
                dbc.Button(button_text, id=button_id, color="primary", className="me-1")
            ], width=6)
        ], justify="center"),
        html.Div(id="login-register-output", className="mt-2", style={
            "word-wrap": "break-word",
        })
    ])

def notes_page():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("Notes Page"),
                # Other content for the notes page
            ])
        ], justify="center")
    ])

app.layout = dbc.Container([
    dcc.Store(id='login-state', storage_type='local'),  # 存储登录状态
    dcc.Location(id='url', refresh=False),
    create_navbar(),
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'),
    [Input('login-link', 'n_clicks'),
     Input('register-link', 'n_clicks'),
     Input('notes-link', 'n_clicks'),
     Input('logout-link', 'n_clicks')],
    [State('login-state', 'data')]
)
def display_page(login_clicks, register_clicks, notes_clicks, logout_clicks, login_state):
    ctx = callback_context

    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "login-link":
        return create_login_register_form(is_register=False)
    elif button_id == "register-link":
        return create_login_register_form(is_register=True)
    elif button_id == "notes-link" and login_state and isinstance(login_state, dict) and login_state.get('logged_in'):
        return notes_page()
    elif button_id == "logout-link":
        return html.Div()
    else:
        return html.Div()

@app.callback(
    [Output('login-state', 'data'),
     Output('url', 'pathname')],
    [Input({'type': 'auth-button', 'index': ALL}, 'n_clicks'),
     Input('logout-link', 'n_clicks')],
    [State('username', 'value'),
     State('password', 'value')]
)
def handle_auth_buttons(n_clicks, logout_clicks, username, password):
    ctx = callback_context

    if not ctx.triggered:
        return dash.no_update, dash.no_update

    button_id = ctx.triggered[0]['prop_id']

    if 'auth-button' in button_id:
        button_index = button_id.split('"index":"')[1].split('","type":"')[0]
        if not username or not password:
            print("Username or password missing")
            return dash.no_update, dash.no_update

        print(f"Button clicked: {button_index}")
        print(f"Username: {username}, Password: {password}")

        if button_index == "login":
            response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
            if response.status_code == 200:
                print("Login successful")
                return {"logged_in": True, "username": username}, "/notes"
            else:
                print(f"Login failed: {response.text}")
                return dash.no_update, dash.no_update

        elif button_index == "register":
            response = requests.post(f"{API_URL}/register", json={"username": username, "password": password})
            if response.status_code == 201:
                print("Registration successful")
                return {"logged_in": True, "username": username}, "/notes"
            else:
                print(f"Registration failed: {response.text}")
                return dash.no_update, dash.no_update

    elif 'logout-link' in button_id and logout_clicks:
        print("Logout clicked")
        return {"logged_in": False, "username": None}, "/"

    return dash.no_update, dash.no_update

@app.callback(
    Output('login-register-output', 'children'),
    [Input({'type': 'auth-button', 'index': ALL}, 'n_clicks')],
    [State('username', 'value'),
     State('password', 'value')]
)
def update_output_message(n_clicks, username, password):
    ctx = callback_context

    if not ctx.triggered:
        return ""

    button_id = ctx.triggered[0]['prop_id']

    if 'auth-button' in button_id:
        button_index = button_id.split('"index":"')[1].split('","type":"')[0]

        if button_index == "login":
            if not username or not password:
                return "Username or password missing"
            response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
            if response.status_code == 200:
                return "Login successful!"
            else:
                return f"Login failed: {response.text}"

        elif button_index == "register":
            if not username or not password:
                return "Username or password missing"
            response = requests.post(f"{API_URL}/register", json={"username": username, "password": password})
            if response.status_code == 201:
                return "Registration successful!"
            else:
                return f"Registration failed: {response.text}"

    return ""

@app.callback(
    [Output('login-link', 'style'),
     Output('register-link', 'style'),
     Output('notes-link', 'style'),
     Output('logout-link', 'style')],
    [Input('login-state', 'data')]
)
def update_nav_links(login_state):
    if login_state and isinstance(login_state, dict) and login_state.get('logged_in'):
        return hide_style, hide_style, show_style, show_style
    else:
        return show_style, show_style, hide_style, hide_style

if __name__ == '__main__':
    app.run_server(debug=True)
