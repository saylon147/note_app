import requests
from dash import html, Input, State, Output, no_update
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from flask import session

# TODO 翻页用 Pagination 看看要不要结合使用 Tabs 作为顶部的分类

API_URL = "http://localhost:5000/api"

notes_list = [
    {
        "id": "1",
        "title": "Note 一",
        "tag": "tag1",
        "content": "随便写一些文字"
    },
    {
        "id": "2",
        "title": "Note 二",
        "tag": "tag1,tag2",
        "content": "随便写一些文字随便写一些文字随便写一些文字"
    },
    {
        "id": "3",
        "title": "Note 三",
        "tag": "tag2",
        "content": "随便写一些文字随便写一些文字"
    },
    {
        "id": "4",
        "title": "Note 四",
        "tag": "tag3",
        "content": "随便写一些文字随便写一些文字随便写一些文字随便写一些文字随便写一些文字随便写一些文字随便写一些文字随便写一些文字"
    },
]


def create_note_card(note):
    return dmc.Card(children=[
        dmc.Text(note.get("title"), fw=500),
        dmc.Text(note.get("content"), size="sm", c="dimmed"),
    ],
        withBorder=True,
        shadow="sm",
        radius="md",
        w=300, h=200,
    )


def notes_page():
    span_value = "auto"  # 一行是12，span=6的话，就是一行2个；span是4的话，就是一行3个
    note_cards = [
        dmc.GridCol(
            create_note_card(note), span=span_value
        ) for note in notes_list
    ]
    note_cards.append(
        dmc.GridCol(
            dmc.Center(children=[dmc.Button("Add Note", id="open-add-note-btn")]),
            span=span_value, w=300, h=200,
        )
    )

    return html.Div([
        dmc.Title(f"Notes Page", order=1),
        html.Br(),
        dmc.Modal(
            id="add-note-modal",
            title="Add Note",
            zIndex=10000,
            children=[
                dmc.Stack(children=[
                    dmc.TextInput(label="Title", id="new-note-title", required=True),
                    dmc.TagsInput(label="Tags", id="new-note-tags", required=True, value=[], mb=10),
                    dmc.Textarea(label="Content", id="new-note-content", required=True, autosize=True, minRows=3),
                    dmc.Button("Add", id="new-note-btn"),
                ]),
            ],
            closeOnClickOutside=False,
        ),

        dmc.Grid(
            children=note_cards,
            gutter="xl", justify="flex-start", align="stretch"
        ),
    ])


def register_callback_notes(app):
    @app.callback(
        Output("add-note-modal", "opened"),
        [Input("open-add-note-btn", "n_clicks"),
         Input("new-note-btn", "n_clicks")],
        [State("add-note-modal", "opened"),
         State("new-note-title", "value"),
         State("new-note-tags", "value"),
         State("new-note-content", "value")],
        prevent_init_call=True,
    )
    def add_note(open_clicks, new_note_clicks, opened, title, tags, content):
        if open_clicks and not opened:
            return True
        if new_note_clicks:
            if title and tags and content:
                print("post note")
                response = requests.post(f"{API_URL}/notes",
                                         json={"title": title, "content": content, "tags": tags})
                if response.status_code == 201:
                    msg = response.json()["msg"]
                    print(msg)
                    return False
                else:
                    print(response.status_code)
                    return no_update
        return no_update
