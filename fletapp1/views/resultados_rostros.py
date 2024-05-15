import flet as ft
from flet import ElevatedButton, Column, Row
from flet_route import Params, Basket
from state import state
import os

def ResultadosRostros(page: ft.Page, params: Params, basket: Basket):
    image_files = [
        'views/functions/Rostros capturados/rostro_0.jpg',
        'views/functions/Rostros capturados/rostro_1.jpg',
        'views/functions/Rostros capturados/rostro_2.jpg'
    ]

    images = [ft.Image(src=image) for image in image_files]

    def repetir():
        for i in range(3):
            os.remove(f'views/functions/Rostros capturados/rostro_{i}.jpg')
        state.captura_de_camara.count = 0
        state.captura_de_camara.visible = False
        page.go("/user_id/examenes/:exam_id/identificacion_facial")

    def confirmar():
        print("Confirmar presionado")

    repetir_button = ElevatedButton(text="Repetir", on_click=lambda _: repetir())
    confirmar_button = ElevatedButton(text="Confirmar", on_click=lambda _: confirmar())

    return ft.View(
        "/user_id/examenes/:exam_id/identificacion_facial/resultados_rostros",
        controls=[
            Column(images),
            Row([repetir_button, confirmar_button])
        ]
    )
