class SharedState:
    def __init__(self):
        self.user_id = None
        self.user_email = None
        self.user_role = None
        self.control_acceso_id = None
        self.captura_de_camara_facial = None
        self.captura_de_camara_codigo = None
        self.images_paths_array = []
        self.facial_v = None
        self.code_v = None
        self.codigo_detectado = None

state = SharedState()
