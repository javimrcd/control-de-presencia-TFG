class SharedState:
    def __init__(self):
        self.user_id = None
        self.user_email = None
        self.user_role = None
        self.examen_id = None
        self.control_acceso_id = None
        self.captura_de_camara_facial = None
        self.captura_de_camara_codigo = None
        self.images_paths_array = []
        self.facial_v = None
        self.code_v = None
        self.codigo_detectado = None

        self.examen_iniciado_caso1 = False # servirá para saber si se ha hecho el control del inicio del examen, en el caso de que el examen requiera solo control al inicio.
        self.examen_finalizado_caso2 = False # servirá para saber si se ha hecho el control del final del examen, en el caso de que el examen requiera control solo al final.
        self.examen_iniciado_caso3 = False # servirá para saber si se ha hecho el control del inicio del examen en el caso del control al inicio y al final.
        self.examen_finalizado_caso3 = False # servirá para saber si se ha hecho el control del final del examen en el caso del control al inicio y al final.

state = SharedState()
