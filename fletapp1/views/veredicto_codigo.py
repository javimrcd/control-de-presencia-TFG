import flet as ft
from flet import ElevatedButton, Column, Text
from flet_route import Params, Basket
from state import state

def ResultadoVeredictoCodigo(page: ft.Page, params: Params, basket: Basket):
    veredicto_codigo = state.code_v

    resultado_text = Text("Resultado enviado", size=25, weight="bold")
    veredicto_final_facial_text = Text(f"Veredicto: {veredicto_codigo}")

    examenes_button: ElevatedButton = ElevatedButton(text="Exámenes", on_click=lambda _: page.go("/user_id/examenes/"))

    return ft.View(
        "/:user_id/examenes/:exam_id/identificacion_facial/veredicto_codigo_resultados",
        controls={
            Column(controls=[
                resultado_text,
                veredicto_final_facial_text,
                examenes_button
            ])
        }
    )