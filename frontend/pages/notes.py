import requests
from dash import html, Input, State, Output
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from flask import session

# TODO 翻页用 Pagination 看看要不要结合使用 Tabs 作为顶部的分类
# 结合 Grid 和 Card 来做展示

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


# def create_accordion_label(label, description):
#     return dmc.AccordionControl(
#         dmc.Group(
#             [
#                 # dmc.Avatar(src=image, radius="xl", size="lg"),
#                 html.Div(
#                     [
#                         dmc.Text(label),
#                         dmc.Text(description, size="sm", fw=400, c="dimmed"),
#                     ]
#                 ),
#             ]
#         )
#     )
#
#
# def create_accordion_content(content):
#     return dmc.AccordionPanel(dmc.Text(content, size="sm"))


def create_note_card(note):
    return dmc.Card(children=[
        dmc.Text(note.get("title"), fw=500),
        dmc.Text(note.get("content"), size="sm", c="dimmed"),
    ],
        withBorder=True,
        shadow="sm",
        radius="md",
        w=300,
        h=200,
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
            dmc.Center(children=[dmc.Button("Add Note")]),
            span=span_value, w=300, h=200,
        )
    )

    return html.Div([
        dmc.Title(f"Notes Page", order=1),
        html.Br(),

        dmc.Grid(
            children=note_cards,
            gutter="xl", justify="flex-start", align="stretch"
        ),

        # dmc.Accordion(
        #     chevronPosition="right",
        #     variant="contained",
        #     children=[
        #         dmc.AccordionItem([
        #             create_accordion_label(note["title"], note["tag"]),
        #             create_accordion_content(note["content"])
        #         ], value=note["id"],)
        #         for note in notes_list
        #     ]
        # ),
    ])


def register_callback_notes(app):
    pass
