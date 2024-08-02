from urllib.parse import parse_qs, urlparse

from dash import Output, Input, html

from pages.home import home_page
from pages.login import login_page, register_callback_login
from pages.register import register_page, register_callback_register
from pages.notes import notes_page, register_callback_notes
from pages.reset_pwd import reset_pwd_page, register_callback_reset_pwd


def register_callbacks(app):
    @app.callback(
        Output("page-content", "children"),
        [Input("url", "pathname"),
         Input("url", "search"),]
    )
    def render_page_content(pathname, search):
        if pathname == "/":
            return home_page()
        elif pathname == "/login":
            return login_page()
        elif pathname == "/register":
            return register_page()
        elif pathname == "/resetpwd":
            query_params = parse_qs(urlparse(search).query)
            username = query_params.get('username', [''])[0]
            return reset_pwd_page(username)
        elif pathname == "/notes":
            return notes_page()
        else:
            return html.Div(
                [
                    html.H1("404: Not found", className="text-danger"),
                ],
                className="p-3 bg-light rounded-3",
            )

    register_callback_login(app)
    register_callback_register(app)
    register_callback_reset_pwd(app)
    register_callback_notes(app)
