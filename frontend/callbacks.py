from dash import Output, Input, html

from pages.home import home_page
from pages.login import login_page, register_callback_login
from pages.register import register_page, register_callback_register
from pages.notes import notes_page, register_callback_notes


def register_callbacks(app):
    @app.callback(
        Output("page-content", "children"),
        Input("url", "pathname")
    )
    def render_page_content(pathname):
        if pathname == "/":
            return home_page()
        elif pathname == "/login":
            return login_page()
        elif pathname == "/register":
            return register_page()
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
    register_callback_notes(app)
