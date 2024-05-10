import flet as ft
from flet_route import Params, Basket

def Home(page: ft.Page, params: Params, basket: Basket):
    
    return ft.View(
        "/",

        controls = [
            ft.Text("Home view"),
            # ft.ElevatedButton("Examenes", on_click=lambda _: page.go("/01/examenes")),
            # INCLUIR UN LOGOUT
            ft.ElevatedButton("Login", on_click=lambda _: page.go("/login")),
        ]
        
    )
         