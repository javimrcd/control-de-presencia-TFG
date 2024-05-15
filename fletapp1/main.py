import flet as ft
from flet_route import Routing, path
from views.home import Home
from views.login import Login
from views.examenes import Examenes

from views.identificacion_facial import Facial
from views.captura_de_camara_facial import CapturaDeCamara_Facial
from views.resumen_rostros import ResumenRostros
from views.veredicto_facial import ResultadoVeredictoFacial

from views.identificacion_codigo import Codigo
from views.captura_de_camara_codigo import CapturaDeCamara_Codigo
from views.resumen_codigo import ResumenCodigo
from views.veredicto_codigo import ResultadoVeredictoCodigo


def main(page: ft.Page):
    page.title = 'App'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 300
    page.window_height = 600
    page.window_resizable = True


    app_routes = [
        # path(url="/", clear = True, view=Home),
        path(url="/login", clear = True, view=Login),
        path(url="/:user_id/examenes/", clear = True, view=Examenes),
        path(url="/:user_id/examenes/:exam_id/identificacion_facial", clear = True, view=Facial),
        path(url="/:user_id/examenes/:exam_id/identificacion_facial/resumen_rostros", clear = True, view=ResumenRostros),       
        path(url="/:user_id/examenes/:exam_id/identificacion_facial/veredicto_facial_resultados", clear = True, view=ResultadoVeredictoFacial),
        path(url="/:user_id/examenes/:exam_id/identificacion_codigo", clear = True, view=Codigo),
        path(url="/:user_id/examenes/:exam_id/identificacion_codigo/resumen_codigo", clear = True, view=ResumenCodigo),
        path(url="/:user_id/examenes/:exam_id/identificacion_facial/veredicto_codigo_resultados", clear = True, view=ResultadoVeredictoCodigo)
    ]

    Routing(page=page, app_routes=app_routes)
    page.go("/:user_id/examenes/:exam_id/identificacion_codigo")

ft.app(target = main)