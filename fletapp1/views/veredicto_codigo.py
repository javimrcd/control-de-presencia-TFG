import flet as ft
from flet import ElevatedButton, Column, Text
from flet_route import Params, Basket
from state import state
from firebase_config import db

def ResultadoVeredictoCodigo(page: ft.Page, params: Params, basket: Basket):
    user_id = state.user_id
    control_acceso_id = state.control_acceso_id
    examen_id = state.examen_id
    veredicto_codigo = state.code_v


    def continuar():
        examen_ref = db.collection('examenes').document(examen_id).get()
        examen_data = examen_ref.to_dict()
        control_inicial = examen_data.get('control_inicial', False)
        control_final =examen_data.get('control_final', False)
        
        if ((control_inicial == True) and (control_final == False)):
            page.go(f"/{user_id}/examenes_alumno/{control_acceso_id}/examen_iniciado")
        elif ((control_inicial == False) and (control_final == True)):
            page.go(f"/{user_id}/examenes_alumno/{control_acceso_id}/examen_finalizado")
        else:
            if state.examen_iniciado_caso3 == False:
                page.go(f"/{user_id}/examenes_alumno/{control_acceso_id}/examen_iniciado")
            else:
                page.go(f"/{user_id}/examenes_alumno/{control_acceso_id}/examen_finalizado")



    resultado_text = Text("Resultado enviado", size=25, weight="bold")
    veredicto_codigo_text = Text(f"Veredicto: {veredicto_codigo}")

    continue_button: ElevatedButton = ElevatedButton(text="Continuar", on_click=lambda _: continuar())


    variables_state = ft.Column([
        ft.Text(value=f"Examen iniciado caso 1: {state.examen_iniciado_caso1}"),
        ft.Text(value=f"Examen finalizado caso 2: {state.examen_finalizado_caso2}"),
        ft.Text(value=f"Examen iniciado caso 3: {state.examen_iniciado_caso3}"),
        ft.Text(value=f"Examen finalizado caso 3: {state.examen_finalizado_caso3}")
    ])


    return ft.View(
        f"/{user_id}/examenes_alumno/{control_acceso_id}/identificacion_codigo/veredicto_codigo_resultados",
        controls={
            Column(controls=[
                resultado_text,
                veredicto_codigo_text,
                variables_state,
                continue_button
            ])
        }
    )