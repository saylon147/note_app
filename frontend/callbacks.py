import requests
from dash import Input, Output, State, no_update
from pages.user_operate import login_page, register_page, logout_page
from pages.notes import notes_page
from pages.home import home_page

AUTH_URL = "http://localhost:5000/auth/"
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
        elif pathname == '/register':
            return register_page(), pathname
        elif pathname == '/notes' and login_state:
            return notes_page(), pathname
        elif pathname == '/logout' and login_state:
            return logout_page(), pathname

        # 默认页面是首页
        return home_page(), '/'

    @app.callback(
        [Output('login-state', 'data'),
         Output('url', 'href'),
         Output('dummy-div', 'children')],
        [Input('login-button', 'n_clicks')],
        [State('username', 'value'),
         State('password', 'value'),
         State('login-button', 'children')],
        prevent_initial_call=True
    )
    def user_operate(login_clicks, username, password, login_btn):
        print(login_clicks, username, password, login_btn)
        if login_clicks:
            if login_btn == "Login":
                print("do login")
                response = requests.post(f"{AUTH_URL}login",
                                         json={"username": username, "password": password})
                if response.status_code == 200:
                    print("login success")
                    # token = response.json()["access_token"]
                    return True, '/notes', 'Login successful'
                else:
                    print(f"Login failed: {response.text}")
                    return False, no_update, 'Login failed'
            elif login_btn == "Register":
                print("do register")
                response = requests.post(f"{AUTH_URL}register",
                                         json={"username": username, "password": password})
                if response.status_code == 201:
                    print("register success")
                    return True, '/notes', 'Register successful'
                else:
                    print(f"Register failed: {response.text}")
                    return False, no_update, 'Login failed'
            elif login_btn == "Logout":
                return False, '/', 'Logout'

        return no_update, no_update, no_update


