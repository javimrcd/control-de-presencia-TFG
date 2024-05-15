import flet as ft
from flet import ElevatedButton, Column, Text
from flet_route import Params, Basket
from state import state



def ResultadoVeredictoFacial(page: ft.Page, params: Params, basket: Basket):
    veredicto_final_facial = state.facial_v

    def continuar():
        page.go("/:user_id/examenes/:exam_id/identificacion_codigo")

    resultado_text = Text("Resultado enviado", size=25, weight="bold")
    veredicto_final_facial_text = Text(f"Veredicto: {veredicto_final_facial}")

    continuar_button = ElevatedButton(text="Continuar", on_click=lambda _: continuar())

    return ft.View(
        "/:user_id/examenes/:exam_id/identificacion_facial/veredicto_facial_resultados",
        controls={
            Column(controls=[
                resultado_text,
                veredicto_final_facial_text,
                continuar_button
            ])
        }
    )