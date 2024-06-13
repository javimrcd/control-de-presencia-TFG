import cv2
import numpy as np
import flet as ft
import base64
import threading
from state import state
from firebase_config import storage, db

class CapturaDeCamara_Facial(ft.UserControl):
    def __init__(self, user_id, control_acceso_id, on_complete_callback):
        super().__init__()
        self.user_id = user_id
        self.control_acceso_id = control_acceso_id
        self.camera_running = False
        self.camera_lock = threading.Lock()
        self.capture_face = False
        self.max_rostros = 3
        self.faceClassif = cv2.CascadeClassifier('C:/Programas/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml')
        self.count = 0
        self.on_complete_callback = on_complete_callback

    def camara(self):
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
                        if state.examen_iniciado_caso3:
                            image_path = f"rostro_{self.count + 3}.jpg"
                        else:
                            image_path = f"rostro_{self.count}.jpg"
                        state.images_paths_array.append(image_path)
                        cv2.imwrite(image_path, rostro)
                        print(f"Rostro {self.count} detectado y capturado")
                        self.count += 1
                        self.capture_face = False
                        if self.count >= self.max_rostros:
                            self.on_complete_callback()
                            self.stop_camera()
                            return
                else:
                    self.capture_face = False
                    print("Cuidado, ha querido hacer una foto mientras no se detectaba un rostro")
                
        cap.release()

    def start_camera(self):
        with self.camera_lock:
            self.camera_running = True
            threading.Thread(target=self.camara).start()

    def stop_camera(self):
        with self.camera_lock:
            self.camera_running = False

    def build(self):
        self.img = ft.Image(
            border_radius=ft.border_radius.all(20)
        )
        return self.img