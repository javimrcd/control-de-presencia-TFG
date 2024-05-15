import flet as ft
from flet import ElevatedButton, Text, Column, Row
from flet_route import Params, Basket
from state import state
import os


def ResumenCodigo(page: ft.Page, params: Params, basket: Basket):
    # Imágenes a mostrar de los rostros capturados
    code_picture = 'views/functions/Codigos capturados/codigo.jpg'

    image = ft.Image(src=code_picture, border_radius=ft.border_radius.all(20))

    # FUNCIONES DE LOS BOTONES
    def repetir():
        os.remove('views/functions/Codigos capturados/codigo.jpg')
        state.captura_de_camara_codigo = False
        page.go("/user_id/examenes/:exam_id/identificacion_codigo")

    def confirmar():

        def verify_code(captured_code):
            with open("views/functions/codigos.txt", "r") as f:
                codigos = f.read().splitlines()
                return captured_code in codigos

        state.code_v = verify_code(state.codigo_detectado)

        page.go("/:user_id/examenes/:exam_id/identificacion_facial/veredicto_codigo_resultados")


    # BOTONES DE LA VISTA RESUMEN
    repetir_button = ElevatedButton(text="Repetir", on_click=lambda _: repetir())
    confirmar_button = ElevatedButton(text="Confirmar", on_click=lambda _: confirmar())
    codigo_detectado_text = Text(f"Código detectado : {state.codigo_detectado}")

    return ft.View(
        "/:user_id/examenes/:exam_id/identificacion_facial/resumen_codigo",
        controls=[
            image,
            codigo_detectado_text,
            Row([repetir_button, confirmar_button])
        ]
    )
