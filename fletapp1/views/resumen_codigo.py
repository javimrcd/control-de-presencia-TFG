import flet as ft
from flet import ElevatedButton, Text, Column, Row
from flet_route import Params, Basket
from state import state
import os
from firebase_config import db, bucket


def ResumenCodigo(page: ft.Page, params: Params, basket: Basket):
    user_id = state.user_id
    control_acceso_id = state.control_acceso_id
    examen_id = state.examen_id

    # Obtener el profesor que ha propuesto ese examen
    teacher_doc = db.collection('examenes').document(examen_id).get()
    if teacher_doc.exists:
        teacher_data = teacher_doc.to_dict()
        teacher_id = teacher_data.get('profesor', "")
    else:
        teacher_id = ""

    # Imagen del rostro capturado
    if not state.examen_iniciado_caso1 or not state.examen_iniciado_caso3:
        code_picture = 'views/functions/Codigos capturados/codigo_inicial.jpg'

    elif not state.examen_finalizado_caso2 or state.examen_iniciado_caso3:
        code_picture = 'views/functions/Codigos capturados/codigo_final.jpg'
   

    image = ft.Image(src=code_picture, border_radius=ft.border_radius.all(20))

    # FUNCIONES DE LOS BOTONES
    def repetir():
        os.remove(code_picture)
        state.captura_de_camara_codigo = False
        page.go(f"/{user_id}/examenes_alumno/{control_acceso_id}/identificacion_codigo")

    def confirmar():
        examen_ref = db.collection('examenes').document(examen_id).get()
        examen_data = examen_ref.to_dict()
        control_inicial = examen_data.get('control_inicial', False)
        control_final =examen_data.get('control_final', False)

        codigos_file_path = f"usuarios/{teacher_id}/examenes/{examen_id}/codigos.txt"

        # Descargar el archivo codigos.txt con el que se va a comparar el código detectado, a una ubicación local temporal
        temp_codigos_file = f"temp_codigos.txt"
        blob = bucket.blob(codigos_file_path)
        blob.download_to_filename(temp_codigos_file)

        def verify_code(captured_code):
            with open(temp_codigos_file, "r") as f:
                codigos = f.read().splitlines()
                return captured_code in codigos

        state.code_v = verify_code(state.codigo_detectado)

        # Subir foto del codigo al Storage y actualizar control de acceso.
        if not state.examen_iniciado_caso1 or not state.examen_iniciado_caso3:
            blob = bucket.blob(f"usuarios/{user_id}/controles_acceso/{control_acceso_id}/codigo_inicial.jpg")

        elif not state.examen_finalizado_caso2 or state.examen_iniciado_caso3:
            blob = bucket.blob(f"usuarios/{user_id}/controles_acceso/{control_acceso_id}/codigo_final.jpg")
        
        blob.upload_from_filename(code_picture)
        blob.make_public()
        image_url = blob.public_url

        if ((control_inicial == True) and (control_final == False)):
            db.collection('controles_acceso').document(control_acceso_id).update({
                "imagen_4_inicial": image_url,
                "veredicto_codigo_inicial": bool(state.code_v)
            })
        elif ((control_inicial == False) and (control_final == True)):
            db.collection('controles_acceso').document(control_acceso_id).update({
                "imagen_4_final": image_url,
                "veredicto_codigo_final": bool(state.code_v)
            })
        else:
            if state.examen_iniciado_caso3 == False:
                db.collection('controles_acceso').document(control_acceso_id).update({
                    "imagen_4_inicial": image_url,
                    "veredicto_codigo_inicial": bool(state.code_v)
                })
            else:
                db.collection('controles_acceso').document(control_acceso_id).update({
                    "imagen_4_final": image_url,
                    "veredicto_codigo_final": bool(state.code_v)
                })


        # Eliminar la foto del codigo almacenada en local y el archivo temporal de codigos.txt que ya no necesitamos
        os.remove(temp_codigos_file)
        os.remove(code_picture)


        page.go(f"/{user_id}/examenes_alumno/{control_acceso_id}/identificacion_facial/veredicto_codigo_resultados")


    # BOTONES DE LA VISTA RESUMEN
    repetir_button = ElevatedButton(text="Repetir", on_click=lambda _: repetir())
    confirmar_button = ElevatedButton(text="Confirmar", on_click=lambda _: confirmar())
    codigo_detectado_text = Text(f"Código detectado : {state.codigo_detectado}")

    return ft.View(
        f"/{user_id}/examenes_alumno/{control_acceso_id}/identificacion_facial/resumen_codigo",
        controls=[
            image,
            codigo_detectado_text,
            Row([repetir_button, confirmar_button])
        ]
    )
