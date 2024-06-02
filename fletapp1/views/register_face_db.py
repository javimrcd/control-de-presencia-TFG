import cv2
import numpy as np
import flet as ft
import base64
import threading
import os
from state import state
from flet import ElevatedButton
from flet_route import Params, Basket
from firebase_config import db, bucket

class Capture_Face_For_Register(ft.UserControl):
    def __init__(self, user_id, on_complete_callback):
        super().__init__()
        self.camera_running = False
        self.camera_lock = threading.Lock()
        self.capture_face = False
        self.user_id = user_id
        self.on_complete_callback = on_complete_callback
        self.faceClassif = cv2.CascadeClassifier('C:/Programas/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml')

    def camara(self):
        cap = cv2.VideoCapture(0)

        while self.camera_running:
            ret, frame = cap.read()
            if ret:
                gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.faceClassif.detectMultiScale(
                    image=gray_image,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(200, 200),
                    maxSize=(1000, 1000)
                )

                original_frame = frame.copy()
                original_frame = cv2.flip(original_frame, 1)

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

                frame= cv2.flip(frame, 1)
                _, im_arr = cv2.imencode('.png', frame)
                im_b64 = base64.b64encode(im_arr)
                self.img.src_base64 = im_b64.decode("utf-8")
                self.update()

                if self.capture_face:
                    if len(faces) > 0:
                        image_path = f"{self.user_id}.jpg"
                        cv2.imwrite(image_path, original_frame)
                        print("Imagen capturada y guardada en:", image_path)

                        # Subir la imagen a Firebase Storage
                        blob = bucket.blob(f"usuarios/{self.user_id}/perfil.jpg")
                        blob.upload_from_filename(image_path)
                        blob.make_public()
                        profile_image_url = blob.public_url

                        # Actualizar el documento del usuario con la URL de la imagen
                        user_doc = db.collection('usuarios').document(self.user_id)
                        user_doc.update({'imagen_perfil': profile_image_url})

                        os.remove(image_path) # Eliminar la imagen localmente después de subirla


                        self.capture_face = False
                        self.on_complete_callback()
                        self.stop_camera()
                        return
                    else:
                        self.capture_face = False
                        print("No se detectó ningún rostro. Inténtelo de nuevo.")
        cap.release()

    def start_camera(self):
        with self.camera_lock:
            self.camera_running = True
            threading.Thread(target=self.camara).start()

    def stop_camera(self):
        with self.camera_lock:
            self.camera_running = False

    def build(self):
        self.img = ft.Image(border_radius=ft.border_radius.all(20))
        return self.img

def Register_Face(page: ft.Page, params: Params, basket: Basket):
    user_id = params.get('user_id')  # Pasamos el user_id en los params

    def on_capture_complete():
        page.go("/login")

    capturaDeCamara = Capture_Face_For_Register(user_id=user_id, on_complete_callback=on_capture_complete)
    capturaDeCamara.visible = False
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

    on_camara_button_click = lambda _: toggle_camera(camara_button, captura_rostros_button)
    on_captura_rostros_click = lambda _: captura_rostros()

    camara_button = ElevatedButton(text="Abrir cámara", bgcolor="orange", color="white", width=200, on_click=on_camara_button_click)
    captura_rostros_button = ElevatedButton(text="Captura un rostro", bgcolor="green", color="white", width=200, on_click=on_captura_rostros_click, visible=False)
    register_button = ElevatedButton(text="Registrar cara", on_click=lambda _: page.go("/login"))

    return ft.View(
        "/register_face_db",
        controls=[
            ft.Text("Registro facial", size=25, weight="bold"),
            capturaDeCamara,
            camara_button,
            captura_rostros_button,
            register_button
        ]
    )
