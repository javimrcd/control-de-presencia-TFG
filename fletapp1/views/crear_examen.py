import flet as ft
from flet import TextField, Checkbox, ElevatedButton, Text, Column, Row, Dropdown, SnackBar
from flet_core.control_event import ControlEvent
from flet_route import Params, Basket
from state import state
from firebase_config import db
import datetime

def Crear_Examen(page: ft.Page, params: Params, basket: Basket):
    user_id = state.user_id

    # Obtener las asignaturas del profesor desde Firestore
    user_doc = db.collection('usuarios').document(user_id).get()
    if user_doc.exists:
        user_data = user_doc.to_dict()
        asignaturas_del_profesor = user_data.get('asignaturas', [])
    else:
        asignaturas_del_profesor = []

    # Obtener acrónimos de las asignaturas y crear el desplegable
    acronimos_de_asignaturas = {}
    for asignatura_ref in asignaturas_del_profesor:
        asignatura_doc = asignatura_ref.get()
        asignatura_data = asignatura_doc.to_dict()
        acronimos_de_asignaturas[asignatura_ref.id] = asignatura_data.get('acronimo', 'N/A')

    asignatura_dropdown = Dropdown(
        label="Asignatura",
        options=[ft.dropdown.Option(key=asig_id, text=acronimo) for asig_id, acronimo in acronimos_de_asignaturas.items()],
        width=200
    )

    # DatePicker para seleccionar la fecha
    def fecha_seleccionada(e):
        fecha_field.value = fecha_picker.value.strftime("%Y-%m-%d")
        page.update()

    fecha_picker = ft.DatePicker(
        first_date=datetime.datetime(2023, 1, 1),
        last_date=datetime.datetime(2024, 12, 31),
        on_change=fecha_seleccionada,
        expand=True
    )

    fecha_field = TextField(label="Fecha", width=200)
    fecha_button = ElevatedButton(
        "_",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda _: fecha_picker.pick_date()
    )

    page.overlay.append(fecha_picker)

    # TimePicker para seleccionar la hora de inicio
    def hora_inicio_seleccionada(e):
        hora_inicio_field.value = hora_inicio_picker.value.strftime("%H:%M")
        page.update()

    hora_inicio_picker = ft.TimePicker(
        confirm_text="Confirmar",
        error_invalid_text="Hora fuera de rango",
        help_text="Selecciona la hora de inicio",
        on_change=hora_inicio_seleccionada
    )

    hora_inicio_field = TextField(label="Hora de inicio", width=200)
    hora_inicio_button = ElevatedButton(
        "_",
        icon=ft.icons.LOCK_CLOCK,
        on_click=lambda _: hora_inicio_picker.pick_time()
    )

    page.overlay.append(hora_inicio_picker)

    # TimePicker para seleccionar la hora de fin
    def hora_fin_seleccionada(e):
        hora_fin_field.value = hora_fin_picker.value.strftime("%H:%M")
        page.update()

    hora_fin_picker = ft.TimePicker(
        confirm_text="Confirmar",
        error_invalid_text="Hora fuera de rango",
        help_text="Selecciona la hora de fin",
        on_change=hora_fin_seleccionada,
        expand=True
    )

    hora_fin_field = TextField(label="Hora de fin", width=200)
    hora_fin_button = ElevatedButton(
        "_",
        icon=ft.icons.LOCK_CLOCK,
        on_click=lambda _: hora_fin_picker.pick_time()
    )

    page.overlay.append(hora_fin_picker)

    id_facial_checkbox = Checkbox(label="Id. facial", value=False)
    id_codigo_checkbox = Checkbox(label="Id. de código", value=False)
    crear_examen_button = ElevatedButton(text="Crear examen", width=200, disabled=True)
    back_button = ElevatedButton(text="Volver", width=200)

    # Funciones
    def validate(e: ControlEvent) -> None:
        if all([asignatura_dropdown.value, hora_inicio_field.value, hora_fin_field.value, fecha_field.value]):
            crear_examen_button.disabled = False
        else:
            crear_examen_button.disabled = True
        page.update()

    def create(e: ControlEvent) -> None:
        asignatura_id = asignatura_dropdown.value
        asignatura_ref = db.collection('asignaturas').document(asignatura_id)

        examen_data = {
            "asignatura": asignatura_ref,
            "fecha": fecha_field.value,
            "hora_inicio": hora_inicio_field.value,
            "hora_fin": hora_fin_field.value,
            "id_facial": id_facial_checkbox.value,
            "id_codigo": id_codigo_checkbox.value,
            "profesor": user_id
        }

        # Guardar el examen en Firestore
        try:
            db.collection('examenes').add(examen_data)
            page.snack_bar = SnackBar(
                Text("Examen creado con éxito", size=20),
                bgcolor="green"
            )
        except Exception as e:
            page.snack_bar = SnackBar(
                Text(f"Error al crear el examen: {str(e)}", size=20),
                bgcolor="red"
            )
        page.snack_bar.open = True
        page.update()
        page.go(f"/{user_id}/examenes_profesor")

    def volver(e: ControlEvent) -> None:
        page.go(f"/{user_id}/examenes_profesor")

    # Link the functions to our UI
    asignatura_dropdown.on_change = validate
    hora_inicio_field.on_change = validate
    hora_fin_field.on_change = validate
    fecha_field.on_change = validate
    crear_examen_button.on_click = create
    back_button.on_click = volver

    return ft.View(
        f"/{user_id}/examenes_profesor/crear_examen/",
        controls=[
            Column(
                [
                    ft.Text("Crear examen", size=25, weight="bold"),
                    ft.Text(f"Usuario: {state.user_email}", size=15, italic=True),
                    ft.Text(f"Rol: {state.user_role}", size=15, italic=True),
                    asignatura_dropdown,
                    Row([fecha_field, fecha_button]),
                    Row([hora_inicio_field, hora_inicio_button]),
                    Row([hora_fin_field, hora_fin_button]),
                    id_facial_checkbox,
                    id_codigo_checkbox,
                    crear_examen_button,
                    back_button
                ]
            )
        ]
    )
