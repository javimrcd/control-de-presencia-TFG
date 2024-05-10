import flet as ft
from flet import ElevatedButton, Text, Row, Column
from flet_route import Params, Basket
from views.functions.funcion_facial_recognition import reconocimiento_facial

def handle_facial_recognition_click(_=None):
    # Llama a la función de reconocimiento facial
    reconocimiento_facial("Javi")  # Puedes cambiar "Javi" por el nombre de la persona que deseas reconocer


def Facial(page: ft.Page, params: Params, basket: Basket):
    examenes_button: ElevatedButton = ElevatedButton(text="Examenes", on_click=lambda _: page.go("/user_id/examenes/"))
    facial_recognition_button: ElevatedButton = ElevatedButton(text="Cámara", width=200, on_click=handle_facial_recognition_click)
    continue_button: ElevatedButton = ElevatedButton(text="Continuar", width=200, on_click=lambda _: page.go("/user_id/examenes/:exam_id/identificacion_codigo"))

    
    return ft.View(
        "/user_id/examenes/:exam_id/identificacion_facial",

        controls = [
            ft.Text("Identificación facial", weight="bold"),
            examenes_button,
            facial_recognition_button,
            continue_button
        ]
    )
         