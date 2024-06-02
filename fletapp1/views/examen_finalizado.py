import flet as ft
from flet import ElevatedButton, Column, Text
from flet_route import Params, Basket

def ExamenFinalizado(page: ft.Page, params: Params, basket: Basket):

    examenes_button: ElevatedButton = ElevatedButton(text="Exámenes", on_click=lambda _: page.go("/:user_id/examenes_alumno/"))

    return ft.View(
        "/:user_id/examenes_alumno/:exam_id/examen_finalizado",
        controls={
            Column(controls=[
                ft.Text("Examen finalizado con éxito", size=15, weight="bold"),
                ft.Text("Entrega tu examen y abandona el aula.", size=15),
                examenes_button
            ])
        }
    )