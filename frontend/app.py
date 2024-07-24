import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
import requests

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

API_URL = "http://localhost:5000/api"

app.layout = dbc.Container(
    [
        dbc.NavbarSimple(
            brand="Note App",
            brand_href="/",
            color="primary",
            dark=True,
        ),
        dbc.Tabs(
            [
                dbc.Tab(label="Login", tab_id="login"),
                dbc.Tab(label="Register", tab_id="register"),
                dbc.Tab(label="Notes", tab_id="notes"),
            ],
            id="tabs",
            active_tab="login",
        ),
        html.Div(id="tab-content", className="p-4")
    ],
    fluid=True,
)

def login_layout():
    return dbc.Row(
        [
            dbc.Col(
                [
                    html.H2("Login"),
                    dbc.Input(id="login-username", placeholder="Username", type="text"),
                    dbc.Input(id="login-password", placeholder="Password", type="password"),
                    dbc.Button("Login", id="login-button", color="primary", className="mt-2"),
                    html.Div(id="login-output", className="mt-2")
                ],
                width=4,
            ),
        ],
        className="mt-4"
    )

def register_layout():
    return dbc.Row(
        [
            dbc.Col(
                [
                    html.H2("Register"),
                    dbc.Input(id="register-username", placeholder="Username", type="text"),
                    dbc.Input(id="register-password", placeholder="Password", type="password"),
                    dbc.Button("Register", id="register-button", color="primary", className="mt-2"),
                    html.Div(id="register-output", className="mt-2")
                ],
                width=4,
            ),
        ],
        className="mt-4"
    )

def notes_layout():
    return dbc.Row(
        [
            dbc.Col(
                [
                    html.H2("Your Notes"),
                    dbc.Input(id="note-token", placeholder="Token", type="text"),
                    dbc.Button("Load Notes", id="load-notes-button", color="primary", className="mt-2"),
                    html.Div(id="notes-list", className="mt-4"),
                    html.H3("Add a New Note"),
                    dbc.Input(id="note-title", placeholder="Title", type="text"),
                    dbc.Textarea(id="note-content", placeholder="Content"),
                    dbc.Button("Add Note", id="add-note-button", color="primary", className="mt-2"),
                    html.Div(id="add-note-output", className="mt-2")
                ],
                width=8,
            ),
        ],
        className="mt-4"
    )

@app.callback(Output("tab-content", "children"), [Input("tabs", "active_tab")])
def render_tab_content(active_tab):
    if active_tab == "login":
        return login_layout()
    elif active_tab == "register":
        return register_layout()
    elif active_tab == "notes":
        return notes_layout()
    return html.Div("404 - Page not found")

@app.callback(
    Output("login-output", "children"),
    [Input("login-button", "n_clicks")],
    [State("login-username", "value"), State("login-password", "value")]
)
def login(n_clicks, username, password):
    if n_clicks:
        response = requests.post(f"{API_URL}/auth/login", json={"username": username, "password": password})
        if response.status_code == 200:
            token = response.json()["access_token"]
            return f"Login successful. Token: {token}"
        else:
            return "Login failed"
    return ""

@app.callback(
    Output("register-output", "children"),
    [Input("register-button", "n_clicks")],
    [State("register-username", "value"), State("register-password", "value")]
)
def register(n_clicks, username, password):
    if n_clicks:
        response = requests.post(f"{API_URL}/auth/register", json={"username": username, "password": password})
        if response.status_code == 201:
            return "Registration successful"
        else:
            return "Registration failed"
    return ""

@app.callback(
    Output("notes-list", "children"),
    [Input("load-notes-button", "n_clicks")],
    [State("note-token", "value")]
)
def load_notes(n_clicks, token):
    if n_clicks:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}/notes", headers=headers)
        if response.status_code == 200:
            notes = response.json()
            return html.Ul([html.Li(f"Title: {note['title']} - Content: {note['content']}") for note in notes])
        else:
            return "Failed to load notes"
    return ""

@app.callback(
    Output("add-note-output", "children"),
    [Input("add-note-button", "n_clicks")],
    [State("note-token", "value"), State("note-title", "value"), State("note-content", "value")]
)
def add_note(n_clicks, token, title, content):
    if n_clicks:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{API_URL}/notes", json={"title": title, "content": content}, headers=headers)
        if response.status_code == 201:
            return "Note added successfully"
        else:
            return "Failed to add note"
    return ""

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
