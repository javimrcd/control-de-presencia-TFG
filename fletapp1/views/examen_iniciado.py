import flet as ft
from flet import ElevatedButton, Column, Text
from flet_route import Params, Basket
from state import state

def ExamenIniciado(page: ft.Page, params: Params, basket: Basket):
    user_id = state.user_id
    control_acceso_id = state.control_acceso_id


    def iniciar_examen():

        # Actualizar las variables de estado
        state.examen_iniciado_caso1 = True if state.examen_iniciado_caso1 == False else state.examen_iniciado_caso1
        state.examen_iniciado_caso3 = True if state.examen_iniciado_caso3 == False else state.examen_iniciado_caso3


        page.go(f"/{user_id}/examenes_alumno/")

    examenes_button: ElevatedButton = ElevatedButton(text="Exámenes", on_click=lambda _: iniciar_examen())

    return ft.View(
        f"/{user_id}/examenes_alumno/{control_acceso_id}/examen_iniciado",
        controls={
            Column(controls=[
                ft.Text("Examen iniciado con éxito", size=15, weight="bold"),
                ft.Text("Apaga tu teléfono y puedes comenzar el examen.", size=15),
                examenes_button
            ])
        }
    )