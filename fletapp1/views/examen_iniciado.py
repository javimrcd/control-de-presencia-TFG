import flet as ft
from flet import ElevatedButton, Column, Text
from flet_route import Params, Basket

def ExamenIniciado(page: ft.Page, params: Params, basket: Basket):

    examenes_button: ElevatedButton = ElevatedButton(text="Exámenes", on_click=lambda _: page.go("/:user_id/examenes_alumno/"))

    return ft.View(
        "/:user_id/examenes_alumno/:exam_id/examen_iniciado",
        controls={
            Column(controls=[
                ft.Text("Examen iniciado con éxito", size=15, weight="bold"),
                ft.Text("Apaga tu teléfono y puedes comenzar el examen.", size=15),
                examenes_button
            ])
        }
    )