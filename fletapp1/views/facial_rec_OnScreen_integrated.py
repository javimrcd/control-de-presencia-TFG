import cv2
import numpy as np
import flet as ft
from flet import ElevatedButton, Text, Row, Column
from flet_route import Params, Basket
import base64
import threading

class CapturaDeCamara(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.camera_running = False
        self.camera_lock = threading.Lock()
        self.capture_face = False
        self.imagesFoundPath = "views/functions/Rostros capturados/"
        self.max_rostros = 3
        self.faceClassif = cv2.CascadeClassifier('C:/Programas/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml')
        self.count = 0

    def update_timer(self):
        cap = cv2.VideoCapture(0)

        while self.camera_running:
            ret, frame = cap.read()
            gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if self.capture_face == False:
                faces = self.faceClassif.detectMultiScale(
                    image=gray_image,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(200,200),
                    maxSize=(1000,1000))
                
                for (x,y,w,h) in faces:
                    cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0),3)

                frame = cv2.flip(frame, 1)
                _, im_arr = cv2.imencode('.png', frame)
                im_b64 = base64.b64encode(im_arr)
                self.img.src_base64 = im_b64.decode("utf-8")
                self.update()

            else:
                if len(faces) > 0:
                    for (x,y,w,h) in faces:
                        rostro = frame[y:y+h,x:x+w]
                        rostro = cv2.resize(rostro, (150,150), interpolation=cv2.INTER_CUBIC)
                        cv2.imwrite(self.imagesFoundPath+'rostro_{}.jpg'.format(self.count), rostro)
                        print("Rostro "+'rostro_{}.jpg'.format(self.count)+" detectado y capturado")
                        self.count += 1
                        self.capture_face = False
                else:
                    self.capture_face = False
                    print("Cuidado, ha pulsado 's' mientras no se detectaba un rostro")
                
            k = cv2.waitKey(1)

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
    continue_button: ElevatedButton = ElevatedButton(text="Continuar", on_click=lambda _: page.go("/user_id/examenes/:exam_id/identificacion_codigo"))

    return ft.View(
        "/user_id/examenes/:exam_id/identificacion_facial",

        controls = [
            ft.Text("Identificación facial", size=25, weight="bold"),
            capturaDeCamara,
            camara_button,
            captura_rostros_button,
            examenes_button,
            continue_button
        ]
    )
