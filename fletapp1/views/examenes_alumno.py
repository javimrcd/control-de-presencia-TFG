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
        print("Creando examen...")
        # Crear el documento del control de acceso en Firestore
        control_acceso_data = {
            "id_alumno": db.collection('usuarios').document(user_id),
            "id_examen": db.collection('examenes').document(examen['id']),
            "imagen_1": None,
            "veredicto_facial_1": False,
            "imagen_2": None,
            "veredicto_facial_2": False,
            "imagen_3": None,
            "veredicto_facial_3": False,
            "veredicto_facial_final": False,
            "imagen_4": None,
            "veredicto_codigo": False
        }

        control_acceso_ref = db.collection('controles_acceso').add(control_acceso_data)
        print("Examen añadido a la base de datos")
        control_acceso_id = control_acceso_ref[1].id
        state.control_acceso_id = control_acceso_id

        # Navegar a la página de identificación facial
        page.go(f"/{user_id}/examenes_alumno/{control_acceso_id}/identificacion_facial")

    # Crear botones para cada examen
    botones_examenes = []
    for examen in examenes:
        examen_fecha = datetime.strptime(examen['fecha'], "%Y-%m-%d")
        examen_inicio = datetime.strptime(examen['hora_inicio'], "%H:%M").time()
        examen_fin = datetime.strptime(examen['hora_fin'], "%H:%M").time()

        # Verificar si el examen está en el rango de la fecha y hora actual
        clickable = (examen_fecha.date() == now.date() and examen_inicio <= now.time() <= examen_fin)

        def on_button_click(e, ex=examen):
            handle_exam_click(ex)

        boton = ft.ElevatedButton(
            text=f"{examen['acronimo']} - {examen['fecha']}",
            width=150,
            height=50,
            on_click=on_button_click,
            disabled=not clickable
        )
        botones_examenes.append(boton)

    # Crear una parrilla de botones con 2 columnas
    filas = []
    for i in range(0, len(botones_examenes), 2):
        fila = ft.Row([botones_examenes[i], botones_examenes[i+1] if i+1 < len(botones_examenes) else ft.Container()])
        filas.append(fila)

    return ft.View(
        f"/{user_id}/examenes_alumno/",
        controls=[
            ft.Text("Exámenes", size=25, weight="bold"),
            ft.Text(f"Usuario: {state.user_email}", size=15, italic=True),
            ft.Text(f"Rol: {state.user_role}", size=15, italic=True),
            ft.Column(filas),
            ft.ElevatedButton("Logout", on_click=lambda _: page.go("/login")),
        ]
    )
