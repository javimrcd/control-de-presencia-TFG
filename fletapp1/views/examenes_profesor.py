import flet as ft
from flet_route import Params, Basket
from state import state


def Examenes_Profesor(page: ft.Page, params: Params, basket: Basket):

    return ft.View(
        "/:user_id/examenes_profesor/",

        controls = [
            ft.Text("Exámenes", size=25, weight="bold"),
            ft.Text(f"Usuario: {state.user_email}", size=15, italic=True),
            ft.Text(f"Rol: {state.user_role}", size=15, italic=True),
            ft.ElevatedButton("Logout", on_click=lambda _: page.go("/login")),
            ft.ElevatedButton("Crear examen")
        ]
    )
         