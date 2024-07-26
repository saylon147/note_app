import requests
from dash import Input, Output, State, dash
from pages.login import login_page
from pages.notes import notes_page
from pages.home import home_page

API_URL = "http://localhost:5000/api/"


def register_callbacks(app):
    @app.callback(
        Output('page-content', 'children'),
        Output('url', 'pathname'),
        Input('url', 'pathname'),
        State('login-state', 'data')
    )
    def display_page(pathname, login_state):
        print(pathname, login_state)
        if pathname == '/login':
            return login_page(), pathname
        elif pathname == '/notes' and login_state:
            return notes_page(), pathname
        elif pathname == '/logout':
            pass
        # 默认页面是首页
        return home_page(), '/'

    @app.callback(
        [Output('login-state', 'data'), Output('url', 'href')],
        [Input('login-button', 'n_clicks')],
        [State('username', 'value'),
         State('password', 'value')]
    )
    def login(n_clicks, username, password):
        if n_clicks:
            print("do login")
            response = requests.post(f"{API_URL}/auth/login", json={"username": username, "password": password})
            if response.status_code == 200:
                print("login success")
                # token = response.json()["access_token"]
                return True, '/notes'
            else:
                print(f"Login failed: {response.text}")
                return False, dash.no_update
        return dash.no_update, dash.no_update


