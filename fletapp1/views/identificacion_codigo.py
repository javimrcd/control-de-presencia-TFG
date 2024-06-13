import flet as ft
from flet import ElevatedButton, Text
from flet_route import Params, Basket
from views.captura_de_camara_codigo import CapturaDeCamara_Codigo
from state import state

def Codigo(page: ft.Page, params: Params, basket: Basket):
    user_id = state.user_id
    control_acceso_id = state.control_acceso_id

    def on_capture_complete():
        print("Codigo capturado")
        page.go("/:user_id/examenes_alumno/:exam_id/identificacion_codigo/resumen_codigo")

    capturaDeCamaraCodigo = CapturaDeCamara_Codigo(user_id=user_id, control_acceso_id=control_acceso_id, on_complete_callback=on_capture_complete)
    capturaDeCamaraCodigo.visible = False
    state.captura_de_camara_codigo = capturaDeCamaraCodigo

    def toggle_camera(button_open_cam: ElevatedButton, button_photo: ElevatedButton):
        if capturaDeCamaraCodigo.camera_running:
            capturaDeCamaraCodigo.stop_camera()
            capturaDeCamaraCodigo.visible = False
            button_open_cam.text = "Abrir cámara"
            button_photo.visible = False
        else:
            capturaDeCamaraCodigo.start_camera()
            capturaDeCamaraCodigo.visible = True
            button_open_cam.text = "Cerrar cámara"
            button_photo.visible = True
        page.update()

    def captura_codigo():
        capturaDeCamaraCodigo.capture_code = True

    on_camara_button_click = lambda _: toggle_camera(camara_button, captura_codigo_button)
    on_captura_codigo_click = lambda _: captura_codigo()

    camara_button = ElevatedButton(text="Abrir cámara", bgcolor="orange", color="white", width=200, on_click=on_camara_button_click)
    captura_codigo_button = ElevatedButton(text="Captura un código", bgcolor="green", color="white", width=200, on_click=on_captura_codigo_click, visible=False)

    return ft.View(
        "/:user_id/examenes_alumno/:exam_id/identificacion_codigo",
        controls=[
            ft.Text("Identificación por Código", size=25, weight="bold"),
            capturaDeCamaraCodigo,
            camara_button,
            captura_codigo_button,
        ]
    )

         