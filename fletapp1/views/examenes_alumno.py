import flet as ft
from flet_route import Params, Basket
from firebase_config import db
from state import state
from datetime import datetime


def Examenes_Alumno(page: ft.Page, params: Params, basket: Basket):
    user_id = state.user_id

    # Obtener las asignaturas del alumno desde Firestore
    user_doc = db.collection('usuarios').document(user_id).get()
    if user_doc.exists:
        user_data = user_doc.to_dict()
        asignaturas_del_alumno = user_data.get('asignaturas', [])
    else:
        asignaturas_del_alumno = []

    # Obtener los exámenes de las asignaturas del alumno
    examenes = []
    for asignatura_ref in asignaturas_del_alumno:
        examenes_ref = db.collection('examenes').where('asignatura', '==', asignatura_ref).stream()
        for examen in examenes_ref:
            examen_data = examen.to_dict()
            examen_data['id'] = examen.id
            # Obtener el acrónimo de la asignatura
            asignatura_doc = asignatura_ref.get()
            asignatura_data = asignatura_doc.to_dict()
            examen_data['acronimo'] = asignatura_data.get('acronimo', 'N/A')
            examenes.append(examen_data)
    
    # Ordenar los exámenes por fecha
    examenes = sorted(examenes, key=lambda x: x['fecha'])

    # Obtener la fecha y la hora actuales
    now = datetime.now()

    def handle_exam_click(examen):
        control_inicial = examen.get("control_inicial", False)
        control_final = examen.get("control_final", False)

        if control_inicial and control_final:
            # CASO 3: Control doble
            controles_acceso_ref = db.collection('controles_acceso').where('id_alumno', '==', db.collection('usuarios').document(user_id)).where('id_examen', '==', db.collection('examenes').document(examen['id']))
            controles_acceso_docs = list(controles_acceso_ref.stream())

            if not state.examen_iniciado_caso3:
                # Crear un nuevo control de acceso para el inicio
                control_acceso_data = {
                    "id_alumno": db.collection('usuarios').document(user_id),
                    "id_examen": db.collection('examenes').document(examen['id']),
                    "imagen_1_inicial": None,
                    "veredicto_facial_1_inicial": False,
                    "imagen_2_inicial": None,
                    "veredicto_facial_2_inicial": False,
                    "imagen_3_inicial": None,
                    "veredicto_facial_3_inicial": False,
                    "veredicto_facial_definitivo_inicial": False,
                    "imagen_4_inicial": None,
                    "veredicto_codigo_inicial": False
                }
                control_acceso_ref = db.collection('controles_acceso').add(control_acceso_data)
                control_acceso_id = control_acceso_ref[1].id
                state.control_acceso_id = control_acceso_id
                # state.examen_iniciado_caso3 = True
            else:
                # Actualizar el control de acceso existente para el final
                if controles_acceso_docs:
                    control_acceso_doc = controles_acceso_docs[0]
                    control_acceso_id = control_acceso_doc.id
                    db.collection('controles_acceso').document(control_acceso_id).update({
                        "imagen_1_final": None,
                        "veredicto_facial_1_final": False,
                        "imagen_2_final": None,
                        "veredicto_facial_2_final": False,
                        "imagen_3_final": None,
                        "veredicto_facial_3_final": False,
                        "veredicto_facial_definitivo_final": False,
                        "imagen_4_final": None,
                        "veredicto_codigo_final": False
                    })
                    state.control_acceso_id = control_acceso_id
                    # state.examen_finalizado_caso3 = True

        elif control_inicial and not control_final:
            # CASO 1: Control al inicio
            control_acceso_data = {
                "id_alumno": db.collection('usuarios').document(user_id),
                "id_examen": db.collection('examenes').document(examen['id']),
                "imagen_1_inicial": None,
                "veredicto_facial_1_inicial": False,
                "imagen_2_inicial": None,
                "veredicto_facial_2_inicial": False,
                "imagen_3_inicial": None,
                "veredicto_facial_3_inicial": False,
                "veredicto_facial_definitivo_inicial": False,
                "imagen_4_inicial": None,
                "veredicto_codigo_inicial": False
            }
            control_acceso_ref = db.collection('controles_acceso').add(control_acceso_data)
            control_acceso_id = control_acceso_ref[1].id
            state.control_acceso_id = control_acceso_id

        elif not control_inicial and control_final:
            # CASO 2: Control al final
            control_acceso_data = {
                "id_alumno": db.collection('usuarios').document(user_id),
                "id_examen": db.collection('examenes').document(examen['id']),
                "imagen_1_final": None,
                "veredicto_facial_1_final": False,
                "imagen_2_final": None,
                "veredicto_facial_2_final": False,
                "imagen_3_final": None,
                "veredicto_facial_3_final": False,
                "veredicto_facial_definitivo_final": False,
                "imagen_4_final": None,
                "veredicto_codigo_final": False
            }
            control_acceso_ref = db.collection('controles_acceso').add(control_acceso_data)
            control_acceso_id = control_acceso_ref[1].id
            state.control_acceso_id = control_acceso_id


        state.examen_id = examen['id']

        # Actualizar el estado para controlar los flujos de examen
        # if control_inicial and control_final:
        #     state.examen_iniciado_caso3 = False
        #     state.examen_finalizado_caso3 = False
        # elif control_inicial:
        #     state.examen_iniciado_caso1 = False
        # elif control_final:
        #     state.examen_finalizado_caso2 = False
        
        # Redirigir según los parámetros del examen
        if examen['id_facial']:
            page.go(f"/{user_id}/examenes_alumno/{control_acceso_id}/identificacion_facial")
        elif examen['id_codigo']:
            page.go(f"/{user_id}/examenes_alumno/{control_acceso_id}/identificacion_codigo")
        else:
            page.go(f"/{user_id}/examenes_alumno/{control_acceso_id}/examen_iniciado")

    # Crear botones para cada examen
    botones_examenes = []
    for examen in examenes:
        examen_fecha = datetime.strptime(examen['fecha'], "%Y-%m-%d")
        examen_inicio = datetime.strptime(examen['hora_inicio'], "%H:%M").time()
        examen_fin = datetime.strptime(examen['hora_fin'], "%H:%M").time()

        # Verificar si el examen está en el rango de la fecha y hora actual
        clickable = (examen_fecha.date() == now.date() and examen_inicio <= now.time() <= examen_fin)
        texto_boton = ft.Column(
            [
                ft.Text(examen['acronimo'] + " - " + examen['fecha'])
            ],
            alignment=ft.alignment.center
        )
        control_inicial = examen.get("control_inicial", False)
        control_final = examen.get("control_final", False)

        if control_inicial and not control_final:
            if not state.examen_iniciado_caso1:
                texto_boton.controls.append(ft.Text(" - Iniciar examen", color="green"))
            else:
                clickable = False

        if not control_inicial and control_final:
            if not state.examen_finalizado_caso2:
                texto_boton.controls.append(ft.Text(" - Finalizar examen", color="red"))
            else:
                clickable = False

        if control_inicial and control_final:
            if not state.examen_iniciado_caso3:
                texto_boton.controls.append(ft.Text(" - Iniciar examen", color="green"))
            elif not state.examen_finalizado_caso3 and state.examen_iniciado_caso3:
                texto_boton.controls.append(ft.Text(" - Finalizar examen", color="red"))
            else:
                clickable = False


        def on_button_click(e, ex=examen):
            handle_exam_click(ex)

        boton = ft.ElevatedButton(
            content=texto_boton,
            width=100,
            height=100,
            on_click=on_button_click,
            disabled=not clickable
        )
        botones_examenes.append(boton)

    # Crear una parrilla de botones con 2 columnas
    filas = []
    for i in range(0, len(botones_examenes), 2):
        fila = ft.Row([botones_examenes[i], botones_examenes[i+1] if i+1 < len(botones_examenes) else ft.Container()])
        filas.append(fila)


    variables_state = ft.Column([
        ft.Text(value=f"Examen iniciado caso 1: {state.examen_iniciado_caso1}"),
        ft.Text(value=f"Examen finalizado caso 2: {state.examen_finalizado_caso2}"),
        ft.Text(value=f"Examen iniciado caso 3: {state.examen_iniciado_caso3}"),
        ft.Text(value=f"Examen finalizado caso 3: {state.examen_finalizado_caso3}")
    ])

    return ft.View(
        f"/{user_id}/examenes_alumno/",
        controls=[
            ft.Text("Exámenes", size=25, weight="bold"),
            ft.Text(f"Usuario: {state.user_email}", size=15, italic=True),
            ft.Text(f"Rol: {state.user_role}", size=15, italic=True),
            ft.Column(filas),
            variables_state,
            ft.ElevatedButton("Logout", on_click=lambda _: page.go("/login")),
        ]
    )
