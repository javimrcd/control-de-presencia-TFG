import flet as ft
from flet_route import Params, Basket

def Codigo(page: ft.Page, params: Params, basket: Basket):

    return ft.View(
        "/user_id/examenes/:exam_id/identificacion_facial",

        controls = [
            ft.Text("Identificación de código"),
            ft.ElevatedButton("Examenes", on_click=lambda _: page.go("/user_id/examenes/"))
        ]
    )
         