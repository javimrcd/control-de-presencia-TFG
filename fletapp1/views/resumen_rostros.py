import flet as ft
from flet import ElevatedButton, Column, Row
from flet_route import Params, Basket
from state import state
import os
from deepface import DeepFace
from firebase_config import db, bucket

def ResumenRostros(page: ft.Page, params: Params, basket: Basket):
    user_id = state.user_id
    control_acceso_id = state.control_acceso_id
    print(user_id, control_acceso_id)
    image_paths = state.images_paths_array

    images = [ft.Image(src=image, border_radius=ft.border_radius.all(20)) for image in image_paths]

    # FUNCIONES DE LOS BOTONES
    def repetir():
        for image_path in image_paths:
            os.remove(image_path)
        state.captura_de_camara_facial.visible = False
        page.go(f"/{user_id}/examenes_alumno/{control_acceso_id}/identificacion_facial")

    def confirmar():
        nombre = "Javi"
        profile_image_path = f"usuarios/{user_id}/perfil.jpg"

        # Descargar la imagen de perfil del storage a una ubicación local temporal
        temp_profile_image = f"temp_{user_id}_perfil.jpg"
        blob = bucket.blob(profile_image_path)
        blob.download_to_filename(temp_profile_image)

        veredictos_individuales = []
        veredicto_final = False

        # Subir rostros a la DB
        for i, image_path in enumerate(image_paths):
            blob = bucket.blob(f"usuarios/{user_id}/controles_acceso/{control_acceso_id}/rostro_{i}.jpg")
            blob.upload_from_filename(image_path)
            blob.make_public()
            image_url = blob.public_url

            db.collection('controles_acceso').document(control_acceso_id).update({
                f"imagen_{i+1}": image_url
            })

            # Realizar la verificacion facial    
            print('Resultados de verificación individuales:')
        
            resultado_verificacion = DeepFace.verify(
                img1_path = temp_profile_image, 
                img2_path = image_path, 
                detector_backend = "opencv", 
                distance_metric = "cosine", 
                model_name = "VGG-Face", 
                enforce_detection=False
            )
            veredictos_individuales.append((image_path, resultado_verificacion['verified']))

            # Actualizar veredictos individuales en Firestore
            db.collection('controles_acceso').document(control_acceso_id).update({
                f"veredicto_facial_{i+1}": bool(resultado_verificacion['verified'])
            })

            print('Analizando '+f'{image_path}')
            print('Distancia: '+str(resultado_verificacion['distance']))
            print('Umbral: '+str(resultado_verificacion['threshold']))
            print('Veredicto: '+str(resultado_verificacion['verified']))
            print('\n')

        # Eliminar la imagen de perfil descargada temporalmente
        os.remove(temp_profile_image)

        # Calcula el veredicto final
        trues = sum(veredicto for (_, veredicto) in veredictos_individuales)
        falses = len(veredictos_individuales) - trues
        veredicto_final = trues > falses

        state.facial_v = veredicto_final # Guardo el veredicto final en el estado

        # Actualizar veredicto final en Firestore    
        db.collection('controles_acceso').document(control_acceso_id).update({
            "veredicto_facial_final": bool(veredicto_final)
        })

        print('Veredicto final:',veredicto_final)
        
        if veredicto_final:
            print('La persona identificada es:',nombre)
        else:
            print('La persona identificada NO es:',nombre)

        for image_path in image_paths:
            os.remove(image_path)

        page.go(f"/{user_id}/examenes_alumno/{control_acceso_id}/identificacion_facial/veredicto_facial_resultados/")


    # BOTONES DE LA VISTA RESUMEN
    repetir_button = ElevatedButton(text="Repetir", on_click=lambda _: repetir())
    confirmar_button = ElevatedButton(text="Confirmar", on_click=lambda _: confirmar())


    return ft.View(
        "/:user_id/examenes_alumno/:exam_id/identificacion_facial/resumen_rostros",
        controls=[
            Column(images),
            Row([repetir_button, confirmar_button])
        ]
    )
