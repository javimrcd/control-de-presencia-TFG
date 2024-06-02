import flet as ft
from flet import ElevatedButton, Text, Column, Row
from flet_route import Params, Basket
from state import state
import os
from firebase_config import db, bucket


def ResumenCodigo(page: ft.Page, params: Params, basket: Basket):
    user_id = state.user_id
    control_acceso_id = state.control_acceso_id

    # Imágenes a mostrar de los rostros capturados
    code_picture = 'views/functions/Codigos capturados/codigo.jpg'

    image = ft.Image(src=code_picture, border_radius=ft.border_radius.all(20))

    # FUNCIONES DE LOS BOTONES
    def repetir():
        os.remove('views/functions/Codigos capturados/codigo.jpg')
        state.captura_de_camara_codigo = False
        page.go("/user_id/examenes_alumno/:exam_id/identificacion_codigo")

    def confirmar():

        def verify_code(captured_code):
            with open("views/functions/codigos.txt", "r") as f:
                codigos = f.read().splitlines()
                return captured_code in codigos

        state.code_v = verify_code(state.codigo_detectado)

        # Subir foto del codigo al Storage y actualizar control de acceso.
        blob = bucket.blob(f"usuarios/{user_id}/controles_acceso/{control_acceso_id}/codigo.jpg")
        blob.upload_from_filename(code_picture)
        blob.make_public()
        image_url = blob.public_url

        page.go("/:user_id/examenes_alumno/:exam_id/identificacion_facial/veredicto_codigo_resultados")


    # BOTONES DE LA VISTA RESUMEN
    repetir_button = ElevatedButton(text="Repetir", on_click=lambda _: repetir())
    confirmar_button = ElevatedButton(text="Confirmar", on_click=lambda _: confirmar())
    codigo_detectado_text = Text(f"Código detectado : {state.codigo_detectado}")

    return ft.View(
        "/:user_id/examenes_alumno/:exam_id/identificacion_facial/resumen_codigo",
        controls=[
            image,
            codigo_detectado_text,
            Row([repetir_button, confirmar_button])
        ]
    )
