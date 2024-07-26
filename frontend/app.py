import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from callbacks import register_callbacks


# 创建Dash应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True  # 忽略回调异常


# 主布局
app.layout = html.Div([
    # 导航栏
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href='/')),
            dbc.NavItem(dbc.NavLink("Login", href='/login')),
            dbc.NavItem(dbc.NavLink("Notes", href='/notes')),
            dbc.NavItem(dbc.NavLink("Logout", href='/logout')),
        ],
        brand="My Notes",
        brand_href="/",
        color="primary",
        dark=True,
        className="mb-4"
    ),
    dcc.Store(id='login-state', storage_type='local'),  # 存储登录状态
    dcc.Location(id='url', refresh=False),  # 监控URL变化
    html.Div(id='page-content')  # 显示当前页面内容
])


# 注册回调函数
register_callbacks(app)


# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)
