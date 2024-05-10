import flet as ft
from flet import ElevatedButton, Text, Row, Column
from flet_route import Params, Basket

def Facial(page: ft.Page, params: Params, basket: Basket):

    facial_recognition_button: ElevatedButton = ElevatedButton(text="Cámara", width=200)
    continue_button: ElevatedButton = ElevatedButton(text="Continue", width=200, disabled=True)

    

    return ft.View(
        "/user_id/examenes/:exam_id/identificacion_facial",

        controls = [
            ft.Text("Identificación facial"),
            
            ft.ElevatedButton("Examenes", on_click=lambda _: page.go("/user_id/examenes/"))
            # ft.ElevatedButton("Continuar", on_click=lambda _: page.go("/user_id/examenes/:exam_id/identificacion_codigo"))
        ]
    )
         