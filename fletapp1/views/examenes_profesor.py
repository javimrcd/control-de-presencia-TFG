import flet as ft
from flet_route import Params, Basket
from firebase_config import db
from state import state


def Examenes_Profesor(page: ft.Page, params: Params, basket: Basket):
    user_id = state.user_id

    # Obtener los exámenes del profesor desde Firestore
    examenes_ref = db.collection('examenes').where('profesor', '==', user_id).stream()
    examenes = []
    for examen in examenes_ref:
        examen_data = examen.to_dict()
        # Obtener acrónimo de la asignatura desde Firestore
        asignatura_ref = examen_data.get('asignatura')
        asignatura_doc = asignatura_ref.get()
        asignatura_data = asignatura_doc.to_dict()
        examen_data['acronimo'] = asignatura_data.get('acronimo', 'N/A')
        examenes.append(examen_data)

    # Ordenar los exámenes por fecha
    examenes = sorted(examenes, key=lambda x: x['fecha'])

    # Crear botones para cada examen
    botones_examenes = []
    for examen in examenes:
        boton = ft.ElevatedButton(
            text=f"{examen['acronimo']} - {examen['fecha']}",
            width=150,
            height=50,
            on_click=lambda _: None
        )
        botones_examenes.append(boton)

    # Crear una parrilla de botones con 2 columnas
    filas = []
    for i in range(0, len(botones_examenes), 2):
        fila = ft.Row([botones_examenes[i], botones_examenes[i+1] if i+1 < len(botones_examenes) else ft.Container()])
        filas.append(fila)

    return ft.View(
        f"/{user_id}/examenes_profesor/",
        controls=[
            ft.Text("Exámenes del profesor", size=25, weight="bold"),
            ft.Text(f"Usuario: {state.user_email}", size=15, italic=True),
            ft.Text(f"Rol: {state.user_role}", size=15, italic=True),
            ft.Column(filas),
            ft.ElevatedButton("Logout", on_click=lambda _: page.go("/login")),
            ft.ElevatedButton("Crear examen", on_click=lambda _: page.go(f"/{user_id}/examenes_profesor/crear_examen/"))
        ]
    )
         