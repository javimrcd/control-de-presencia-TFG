import cv2
import numpy as np
import flet as ft
import base64
import threading
import easyocr
from state import state

class CapturaDeCamara_Codigo(ft.UserControl):
    def __init__(self, user_id, control_acceso_id, on_complete_callback):
        super().__init__()
        self.user_id = user_id
        self.control_acceso_id = control_acceso_id
        self.camera_running = False
        self.camera_lock = threading.Lock()
        self.capture_code = False
        self.imagesFoundPath = "views/functions/Codigos capturados/"
        self.on_complete_callback = on_complete_callback
        self.reader = easyocr.Reader(["es"], gpu=False)
        self.code_detected = ""

    def camara(self):
        cap = cv2.VideoCapture(0)

        cuadro = 100
        anchocam, altocam = 640, 480

        while self.camera_running:
            ret, frame = cap.read()
            
            # cv2.putText(frame, 'Ubique aqui el texto a leer', (158,80), cv2.FONT_HERSHEY_SIMPLEX, 0.71, (255, 255, 0), 2)
            # cv2.putText(frame, 'Ubique aqui el texto a leer', (160,80), cv2.FONT_HERSHEY_SIMPLEX, 0.71, (0, 0, 0), 2)
            cv2.rectangle(frame, (cuadro, cuadro), (anchocam - cuadro, altocam - cuadro), (0, 0, 0), 2) # Pintamos cuadro
            x1, y1 = cuadro, cuadro
            ancho, alto = (anchocam - cuadro) - x1, (altocam - cuadro) - y1 # Extraemos el ancho y el alto
            x2, y2 = x1 + ancho, y1 + alto # Almacenamos los pixeles del recuadro
            doc = frame[y1:y2, x1:x2]
    
            if ret:
                if self.capture_code:
                    if not state.examen_iniciado_caso1 or not state.examen_iniciado_caso3:
                        cv2.imwrite(self.imagesFoundPath + 'codigo_inicial.jpg', doc)
                    elif not state.examen_finalizado_caso2 or state.examen_iniciado_caso3:
                        cv2.imwrite(self.imagesFoundPath + 'codigo_final.jpg', doc)
                    self.capture_code = False
                    doc = cv2.flip(doc, 1)
                    self.code_detected = self.extract_text(doc)
                    state.codigo_detectado = self.code_detected
                    self.on_complete_callback()
                    self.stop_camera()
                    return

                frame = cv2.flip(frame, 1)
                _, im_arr = cv2.imencode('.png', frame)
                im_b64 = base64.b64encode(im_arr)
                self.img.src_base64 = im_b64.decode("utf-8")
                self.update()

        cap.release()

    def extract_text(self, image):
        gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gris = cv2.flip(gris, 1)
        result = self.reader.readtext(gris)
        for res in result:
            return res[1]
        return ""

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
