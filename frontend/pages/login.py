from dash import html
import dash_bootstrap_components as dbc


def login_page():
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
                           color="primary", className="me-1"),
            ])
        ], justify="center"),
        html.Div(id="login-output", className="mt-2", style={
            # "width": "80%",
            "word-wrap": "break-word",
        })
    ])



