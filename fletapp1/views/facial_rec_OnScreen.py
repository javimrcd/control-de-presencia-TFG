import cv2
import numpy as np
import flet as ft
from flet import ElevatedButton, Text, Row, Column
from flet_route import Params, Basket
import base64
import threading
# import os
# from deepface import DeepFace

class CapturaDeCamara(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.camera_running = False
        self.camera_lock = threading.Lock()

    def update_timer(self):
        cap = cv2.VideoCapture(0)
        while self.camera_running:
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                _, im_arr = cv2.imencode('.png', frame)
                im_b64 = base64.b64encode(im_arr)
                self.img.src_base64 = im_b64.decode("utf-8")
                self.update()
            else:
                break

        cap.release()

    def start_camera(self):
        with self.camera_lock:
            self.camera_running = True
            threading.Thread(target=self.update_timer).start()

    def stop_camera(self):
        with self.camera_lock:
            self.camera_running = False

    def build(self):
        self.img = ft.Image(
            border_radius=ft.border_radius.all(20)
        )
        return self.img

def Facial(page: ft.Page, params: Params, basket: Basket):
    capturaDeCamara = CapturaDeCamara()
    capturaDeCamara.visible = False

    def toggle_camera(button: ElevatedButton):
        if capturaDeCamara.camera_running:
            capturaDeCamara.stop_camera()
            capturaDeCamara.visible = False
            button.text = "Abrir cámara"
        else:
            capturaDeCamara.start_camera()
            capturaDeCamara.visible = True
            button.text = "Cerrar cámara"
        page.update()

    # Función lambda que captura el botón como argumento
    on_camara_button_click = lambda _: toggle_camera(camara_button)

    camara_button: ElevatedButton = ElevatedButton(text="Abrir cámara", bgcolor="orange", color="white", width=200, on_click=on_camara_button_click)
    examenes_button: ElevatedButton = ElevatedButton(text="Exámenes", on_click=lambda _: page.go("/user_id/examenes/"))
    continue_button: ElevatedButton = ElevatedButton(text="Continuar", on_click=lambda _: page.go("/user_id/examenes/:exam_id/identificacion_codigo"))

    return ft.View(
        "/user_id/examenes/:exam_id/identificacion_facial",

        controls = [
            ft.Text("Identificación facial", weight="bold"),
            capturaDeCamara,
            camara_button,
            examenes_button,
            continue_button
            
            
        ]
    )
