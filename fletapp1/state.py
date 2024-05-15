class SharedState:
    def __init__(self):
        self.captura_de_camara_facial = None
        self.captura_de_camara_codigo = None
        self.facial_v = None
        self.code_v = None
        self.codigo_detectado = None

state = SharedState()
