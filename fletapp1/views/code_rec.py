import flet as ft
from flet_route import Params, Basket

def Codigo(page: ft.Page, params: Params, basket: Basket):

    return ft.View(
        "/user_id/examenes/:exam_id/identificacion_facial",

        controls = [
            ft.Text("Identificación de código", size=25, weight="bold"),
            ft.ElevatedButton("Exámenes", on_click=lambda _: page.go("/user_id/examenes/"))
        ]
    )
         