import flet as ft
from flet_route import Routing, path
from views.home import Home
from views.examenes import Examenes
# from views.facial_rec import Facial
from views.facial_rec_OnScreen import Facial
from views.code_rec import Codigo
from views.login import Login

def main(page: ft.Page):
    page.title = 'App'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 300
    page.window_height = 600
    page.window_resizable = True


    app_routes = [
        # path(url="/", clear = True, view=Home),
        path(url="/login", clear = True, view=Login),
        path(url="/user_id/examenes/", clear = True, view=Examenes),
        path(url="/user_id/examenes/:exam_id/identificacion_facial", clear = True, view=Facial),
        path(url="/user_id/examenes/:exam_id/identificacion_codigo", clear = True, view=Codigo)         
    ]

    Routing(page=page, app_routes=app_routes)
    page.go("/login")

ft.app(target = main)