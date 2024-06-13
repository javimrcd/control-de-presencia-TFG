import flet as ft
from flet import TextField, Checkbox, ElevatedButton, Text, Column, Switch, Row, Dropdown, SnackBar
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

    # TextField y DatePicker para seleccionar la fecha
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

    # TimePickers para seleccionar la hora de inicio y fin
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

    # Añadir switches para control al inicio y control al final
    control_inicial_switch = Switch(label="Control al inicio del examen", value=False)
    control_final_switch = Switch(label="Control al final del examen", value=False)
    
    # Texto explicativo que se actualizará según los switches
    texto_explicativo = ft.Text(value="", size=10, italic=True, visible=True)

    # Texto dinámico para mostrar la cantidad de códigos a generar
    texto_codigos = ft.Text(value="Debes seleccionar al menos un control de acceso (inicio o final o ambos).", size=10, italic=True)

    def actualizar_todos_los_textos_y_validar(e: ControlEvent) -> None:
        # Actualizar texto explicativo
        
        if control_inicial_switch.value and control_final_switch.value:
            texto_explicativo.value = "Control doble: Se requerirá un control de acceso al inicio del examen y otro al final."
        elif control_inicial_switch.value:
            texto_explicativo.value = "Control simple: Se requerirá un único control de acceso al inicio del examen."
        elif control_final_switch.value:
            texto_explicativo.value = "Control simple: Se requerirá un único control de acceso al final del examen."
        else:
            texto_explicativo.value = "Debes seleccionar al menos un control de acceso (inicio o final o ambos)."


        # Actualizar texto de códigos
        if id_codigo_checkbox.value:
            asignatura_id = asignatura_dropdown.value
            if asignatura_id:
                asignatura_ref = db.collection('asignaturas').document(asignatura_id)
                asignatura_doc = asignatura_ref.get()
                if asignatura_doc.exists:
                    asignatura_data = asignatura_doc.to_dict()
                    num_alumnos = len(asignatura_data.get('alumnos', []))
                    texto_codigos.value = f"Se generará un PDF con {num_alumnos} códigos."
                    texto_codigos.visible = True
                else:
                    texto_codigos.value = ""
                    texto_codigos.visible = False
            else:
                texto_codigos.value = ""
                texto_codigos.visible = False
        else:
            texto_codigos.value = ""
            texto_codigos.visible = False

        # Validar formulario
        if all([asignatura_dropdown.value, hora_inicio_field.value, hora_fin_field.value, fecha_field.value, (control_inicial_switch.value or control_final_switch.value)]):
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
            "control_inicial": control_inicial_switch.value,
            "control_final": control_final_switch.value,
            "profesor": user_id
        }

        # Guardar el examen en Firestore
        try:
            examen_ref = db.collection('examenes').add(examen_data)
            page.snack_bar = SnackBar(
                Text("Examen creado con éxito", size=20),
                bgcolor="green"
            )
            if id_codigo_checkbox.value:
                examen_id = examen_ref[1].id
                page.go(f"/{user_id}/examenes_profesor/{examen_id}/generar_codigos")
            else:
                page.go(f"/{user_id}/examenes_profesor")
        except Exception as e:
            page.snack_bar = SnackBar(
                Text(f"Error al crear el examen: {str(e)}", size=20),
                bgcolor="red"
            )
        page.snack_bar.open = True
        page.update()

    def volver(e: ControlEvent) -> None:
        page.go(f"/{user_id}/examenes_profesor")


    crear_examen_button = ElevatedButton(text="Crear examen", width=200, disabled=True)
    back_button = ElevatedButton(text="Volver", width=200)

    # Vincular la función combinada a los eventos on_change de los elementos
    id_codigo_checkbox.on_change = actualizar_todos_los_textos_y_validar
    control_inicial_switch.on_change = actualizar_todos_los_textos_y_validar
    control_final_switch.on_change = actualizar_todos_los_textos_y_validar

    # Link the functions to our UI
    asignatura_dropdown.on_change = actualizar_todos_los_textos_y_validar
    hora_inicio_field.on_change = actualizar_todos_los_textos_y_validar
    hora_fin_field.on_change = actualizar_todos_los_textos_y_validar
    fecha_field.on_change = actualizar_todos_los_textos_y_validar
    crear_examen_button.on_click = create
    back_button.on_click = volver

    return ft.View(
        f"/{user_id}/examenes_profesor/crear_examen/",
        controls=[
            Column(
                [
                    ft.Text("Crear examen", size=25, weight="bold"),
                    asignatura_dropdown,
                    Row([fecha_field, fecha_button]),
                    Row([hora_inicio_field, hora_inicio_button]),
                    Row([hora_fin_field, hora_fin_button]),
                    id_facial_checkbox,
                    id_codigo_checkbox,
                    texto_codigos,
                    control_inicial_switch,
                    control_final_switch,
                    texto_explicativo,
                    crear_examen_button,
                    back_button
                ]
            )
        ]
    )

