import flet as ft
from flet import ElevatedButton, Column, Row
from flet_route import Params, Basket
from state import state
import os
from deepface import DeepFace

def ResumenRostros(page: ft.Page, params: Params, basket: Basket):
    # Imágenes a mostrar de los rostros capturados
    image_files = [
        'views/functions/Rostros capturados/rostro_0.jpg',
        'views/functions/Rostros capturados/rostro_1.jpg',
        'views/functions/Rostros capturados/rostro_2.jpg'
    ]
    images = [ft.Image(src=image, border_radius=ft.border_radius.all(20)) for image in image_files]

    # FUNCIONES DE LOS BOTONES
    def repetir():
        for i in range(3):
            os.remove(f'views/functions/Rostros capturados/rostro_{i}.jpg')
        state.captura_de_camara_facial.visible = False
        page.go("/user_id/examenes/:exam_id/identificacion_facial")

    def confirmar():
        nombre = "Javi"
        img_base = "views/functions/Persona/"+nombre+"/"+nombre+".jpg"

        rostros_capturados_path = "views/functions/Rostros capturados/"
        rostros_capturados = os.listdir(rostros_capturados_path)

        veredictos_individuales = []
        veredicto_final = False

        print('Resultados de verificación individuales:')
        for rostro in rostros_capturados:
            # Aplicamos el reconocimiento facial
            resultado_verificacion = DeepFace.verify(
                img1_path = img_base, 
                img2_path = rostros_capturados_path+rostro, 
                detector_backend = "opencv", 
                distance_metric = "cosine", 
                model_name = "VGG-Face", 
                enforce_detection=False
            )
            veredictos_individuales.append((rostro, resultado_verificacion['verified']))

            print('Analizando '+f'{rostro}')
            print('Distancia: '+str(resultado_verificacion['distance']))
            print('Umbral: '+str(resultado_verificacion['threshold']))
            print('Veredicto: '+str(resultado_verificacion['verified']))
            print('\n')

        # Calcula el veredicto final
        trues = sum(veredicto for (_, veredicto) in veredictos_individuales)
        falses = len(veredictos_individuales) - trues
        veredicto_final = trues > falses

        state.facial_v = veredicto_final # Guardo el veredicto final en el estado

        print('Veredicto final:',veredicto_final)
        
        if veredicto_final:
            print('La persona identificada es:',nombre)
        else:
            print('La persona identificada NO es:',nombre)

        page.go("/:user_id/examenes/:exam_id/identificacion_facial/veredicto_facial_resultados/")


    # BOTONES DE LA VISTA RESUMEN
    repetir_button = ElevatedButton(text="Repetir", on_click=lambda _: repetir())
    confirmar_button = ElevatedButton(text="Confirmar", on_click=lambda _: confirmar())


    return ft.View(
        "/:user_id/examenes/:exam_id/identificacion_facial/resumen_rostros",
        controls=[
            Column(images),
            Row([repetir_button, confirmar_button])
        ]
    )
