import flet as ft
from flet import ElevatedButton, Text, Row, Column
from flet_route import Params, Basket
from views.functions.funcion_facial_recognition import reconocimiento_facial

def handle_facial_recognition_click(_=None):
    # Llama a la función de reconocimiento facial
    reconocimiento_facial("Javi")  # Puedes cambiar "Javi" por el nombre de la persona que deseas reconocer


def Facial(page: ft.Page, params: Params, basket: Basket):
    facial_recognition_button: ElevatedButton = ElevatedButton(text="Cámara", width=200)
    continue_button: ElevatedButton = ElevatedButton(text="Continue", width=200, disabled=True)

    
    return ft.View(
        "/user_id/examenes/:exam_id/identificacion_facial",

        controls = [
            ft.Text("Identificación facial", weight="bold"),
            # ft.ElevatedButton("Continuar", on_click=lambda _: page.go("/user_id/examenes/:exam_id/identificacion_codigo"))
            ft.ElevatedButton("Examenes", on_click=lambda _: page.go("/user_id/examenes/")),
            ft.ElevatedButton("Facial Recognition", on_click=handle_facial_recognition_click)
        ]
    )
         