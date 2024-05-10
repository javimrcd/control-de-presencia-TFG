import flet as ft
from flet_route import Params, Basket

def Examenes(page: ft.Page, params: Params, basket: Basket):

    return ft.View(
        "/user_id/examenes/",

        controls = [
            ft.Text("Examenes"),
            ft.ElevatedButton("Logout", on_click=lambda _: page.go("/login")),
            # ft.ElevatedButton("Home", on_click=lambda _: page.go("/")),
            ft.ElevatedButton("Continuar", on_click=lambda _: page.go("/user_id/examenes/:exam_id/identificacion_facial"))
        ]
    )
         