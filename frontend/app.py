from dash import Dash, html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from callbacks import register_callbacks

app = Dash(__name__)
app.config.suppress_callback_exceptions = True  # 忽略回调异常
server = app.server
server.secret_key = '04f69912a0fd7dd7eb0a77954c76573cb71017cc4e179b1ce9ebedac5c1f07f8'


app.layout = dmc.MantineProvider(
    html.Div([
        dcc.Location(id="url"),
        dmc.NotificationProvider(),
        html.Div(id="notifications-container"),

        dmc.Flex([
            html.Div([
                dmc.NavLink(label="Home", leftSection=DashIconify(icon="solar:home-outline"),
                            rightSection=DashIconify(icon="tabler-chevron-right"),
                            href="/", active=True),
                dmc.NavLink(label="Login", leftSection=DashIconify(icon="lets-icons:user-alt"),
                            rightSection=DashIconify(icon="tabler-chevron-right"),
                            href="/login", active=True),
                dmc.NavLink(label="Register", leftSection=DashIconify(icon="lets-icons:user-add"),
                            rightSection=DashIconify(icon="tabler-chevron-right"),
                            href="/register", active=True),
                dmc.NavLink(label="Logout", leftSection=DashIconify(icon="majesticons:logout-line"),
                            rightSection=DashIconify(icon="tabler-chevron-right"),
                            href="/logout", disabled=True),
                dmc.Divider(),
                dmc.NavLink(label="Notes", leftSection=DashIconify(icon="ph:pen-nib-bold"),
                            rightSection=DashIconify(icon="tabler-chevron-right"),
                            href="/notes", active=True),
            ], style={"width": "20%"}),
            html.Div(id='page-content', style={"width": "80%"},),
        ], gap={"base": "lg"}),
    ], style={'margin': '20px'},)
)

register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
