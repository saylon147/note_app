import requests
from dash import html, Input, State, Output
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from flask import session


notes_list = [
    {
        "id": "1",
        "title": "sfyo",
        "tag": "fds",
        "content": "fdsysiysfsf"
    },
    {
        "id": "2",
        "title": "gfdgd",
        "tag": "ffgf",
        "content": "fdsysiys3214fsf"
    },
]


def create_accordion_label(label, description):
    return dmc.AccordionControl(
        dmc.Group(
            [
                # dmc.Avatar(src=image, radius="xl", size="lg"),
                html.Div(
                    [
                        dmc.Text(label),
                        dmc.Text(description, size="sm", fw=400, c="dimmed"),
                    ]
                ),
            ]
        )
    )


def create_accordion_content(content):
    return dmc.AccordionPanel(dmc.Text(content, size="sm"))


def notes_page():
    return html.Div([
        dmc.Title(f"Notes Page", order=1),
        dmc.Accordion(
            chevronPosition="right",
            variant="contained",
            children=[
                dmc.AccordionItem([
                    create_accordion_label(note["title"], note["tag"]),
                    create_accordion_content(note["content"])
                ], value=note["id"],)
                for note in notes_list
            ]
        ),
    ])


def register_callback_notes(app):
    pass
