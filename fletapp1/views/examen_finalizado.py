import flet as ft
from flet import ElevatedButton, Column, Text
from flet_route import Params, Basket
from state import state

def ExamenFinalizado(page: ft.Page, params: Params, basket: Basket):
    user_id = state.user_id
    control_acceso_id = state.control_acceso_id
    examen_id = state.examen_id
    def finalizar_examen():
        

        # Actualizar las variables de estado
        state.examen_finalizado_caso2 = True if state.examen_finalizado_caso2 == False else state.examen_finalizado_caso2
        state.examen_finalizado_caso3 = True if state.examen_finalizado_caso3 == False else state.examen_finalizado_caso3


        page.go(f"/{user_id}/examenes_alumno/")


    examenes_button: ElevatedButton = ElevatedButton(text="Exámenes", on_click=lambda _: finalizar_examen())

    return ft.View(
        f"/{user_id}/examenes_alumno/{control_acceso_id}/examen_finalizado",
        controls={
            Column(controls=[
                ft.Text("Examen finalizado con éxito", size=15, weight="bold"),
                ft.Text("Entrega tu examen y abandona el aula.", size=15),
                examenes_button
            ])
        }
    )