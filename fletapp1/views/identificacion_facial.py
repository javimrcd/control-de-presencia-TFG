import flet as ft
from flet import ElevatedButton
from flet_route import Params, Basket
from views.captura_de_camara_facial import CapturaDeCamara_Facial
from state import state


def Facial(page: ft.Page, params: Params, basket: Basket):

    def on_capture_complete():
        page.go("/:user_id/examenes/:exam_id/identificacion_facial/resumen_rostros")

    capturaDeCamara = CapturaDeCamara_Facial(on_complete_callback=on_capture_complete)
    capturaDeCamara.visible = False
    # Guardar la instancia de CapturaDeCamara en el estado global
    state.captura_de_camara_facial = capturaDeCamara


    def toggle_camera(button_open_cam: ElevatedButton, button_photo: ElevatedButton):
        if capturaDeCamara.camera_running:
            capturaDeCamara.stop_camera()
            capturaDeCamara.visible = False
            button_open_cam.text = "Abrir cámara"
            button_photo.visible = False
        else:
            capturaDeCamara.start_camera()
            capturaDeCamara.visible = True
            button_open_cam.text = "Cerrar cámara"
            button_photo.visible = True
        page.update()

    def captura_rostros():
        capturaDeCamara.capture_face = True

    # Función lambda que captura el botón como argumento
    on_camara_button_click = lambda _: toggle_camera(camara_button, captura_rostros_button)
    on_captura_rostros_click = lambda _: captura_rostros()

    camara_button: ElevatedButton = ElevatedButton(text="Abrir cámara", bgcolor="orange", color="white", width=200, on_click=on_camara_button_click)
    captura_rostros_button: ElevatedButton = ElevatedButton(text="Captura un rostro", bgcolor="green", color="white", width=200, on_click=on_captura_rostros_click, visible=False)
    examenes_button: ElevatedButton = ElevatedButton(text="Exámenes", on_click=lambda _: page.go("/user_id/examenes/"))

    return ft.View(
        "/:user_id/examenes/:exam_id/identificacion_facial",

        controls = [
            ft.Text("Identificación facial", size=25, weight="bold"),
            capturaDeCamara,
            camara_button,
            captura_rostros_button,
            examenes_button
        ]
    )