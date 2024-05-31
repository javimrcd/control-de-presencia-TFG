import flet as ft
from flet import TextField, Checkbox, ElevatedButton, Text, Column, SnackBar
from flet_core.control_event import ControlEvent
from flet_route import Params, Basket
from firebase_config import auth, db
import requests

API_KEY = "AIzaSyDur9r1eePIyCneAq6F3AnxV6SCQkS48uY"

def Register(page: ft.Page, params: Params, basket: Basket):
    
    # Setup our fields
    text_email: TextField = TextField(label="Username", text_align=ft.TextAlign.LEFT, width=200)
    text_password: TextField = TextField(label="Password", text_align=ft.TextAlign.LEFT, width=200, password=True)
    checkbox_signup: Checkbox = Checkbox(label="I agree to stuff", value=False)
    submit_button: ElevatedButton = ElevatedButton(text="Registrarse", width=200, disabled=True)
    text_login: Text = Text(value="¿Ya tienes una cuenta?")
    login_page_button: ElevatedButton = ElevatedButton(text="Iniciar sesión", width=200)

    # functionalities
    def validate(e: ControlEvent) -> None:
        if all([text_email.value, text_password.value, checkbox_signup.value]):
            submit_button.disabled = False
        else:
            submit_button.disabled = True

        page.update()

    def submit(e: ControlEvent) -> None:
        email = text_email.value
        password = text_password.value
        try:
            # Hacer la solicitud a la API de Firebase para registrar un nuevo usuario
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            response = requests.post(url, json=payload)
            response_data = response.json()
            
            if response.status_code == 200:
                user_id = response_data['localId']  # Captura el user_id del usuario registrado

                page.snack_bar = SnackBar(
                    Text(f"Usuario registrado con éxito: {email}", size=20),
                    bgcolor="green"
                )
                page.snack_bar.open = True

                # Guardar el usuario en Firestore
                user_doc = db.collection('usuarios').document(user_id)
                user_doc.set({
                    'email': email,
                    'rol': 'alumno',  # Se asigna el rol de alumno por defecto
                    'imagen_perfil': '',
                    'asignaturas': []
                })

                # Redirigir a la página de registro de cara pasando el user_id
                page.go(f"/register_face_db/{user_id}")
            else:
                raise Exception(response_data["error"]["message"])
        except Exception as e:
            page.snack_bar = SnackBar(
                Text(f"Error: {str(e)}", size=20),
                bgcolor="red"
            )
            page.snack_bar.open = True
        page.update()
     

    def login(e: ControlEvent) -> None:
        page.go("/login")

    # Link the functions to our UI
    checkbox_signup.on_change = validate
    text_email.on_change = validate
    text_password.on_change = validate
    submit_button.on_click = submit
    login_page_button.on_click = login
    

    return ft.View(
        "/register",
        controls=[
            Column(
                [ft.Text("Registro", size=25, weight="bold"),
                text_email,
                text_password,
                checkbox_signup,
                submit_button,
                text_login,
                login_page_button]
            )
        ]
    )



