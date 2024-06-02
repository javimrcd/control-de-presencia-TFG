import flet as ft
from flet import TextField, Checkbox, ElevatedButton, Text, Column, SnackBar
from flet_core.control_event import ControlEvent
from flet_route import Params, Basket
from firebase_config import auth, db
from state import state
import requests


API_KEY = "AIzaSyDur9r1eePIyCneAq6F3AnxV6SCQkS48uY"

def Login(page: ft.Page, params: Params, basket: Basket):
    
    # Setup our fields
    text_email: TextField = TextField(label="Username", text_align=ft.TextAlign.LEFT, width=200)
    text_password: TextField = TextField(label="Password", text_align=ft.TextAlign.LEFT, width=200, password=True)
    checkbox_signup: Checkbox = Checkbox(label="I agree to stuff", value=False)
    submit_button: ElevatedButton = ElevatedButton(text="Entrar", width=200, disabled=True)
    text_signup: Text = Text(value="¿Todavía no tienes una cuenta?")
    signup_button: ElevatedButton = ElevatedButton(text="Registrarse", width=200)

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
            # Hacer la solicitud a la API de Firebase para iniciar sesión
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            response = requests.post(url, json=payload)
            response_data = response.json()
            
            if response.status_code == 200:
                user_id = response_data['localId']
                state.user_id = user_id
                page.snack_bar = SnackBar(
                    Text(f"Usuario autenticado: {email}", size=20),
                    bgcolor="green"
                )
                page.snack_bar.open = True
                
                # Obtener el rol del usuario desde Firestore
                user_doc = db.collection('usuarios').document(user_id).get()
                if user_doc.exists:
                    user_data = user_doc.to_dict()
                    rol_user = user_data.get('rol')

                    # Almacenar el email y rol en el estado
                    state.user_email = email
                    state.user_role = rol_user

                    # Redirigir según el rol del usuario
                    if rol_user == 'profesor':
                        page.go(f"/{user_id}/examenes_profesor/")
                    else:
                        page.go(f"/{user_id}/examenes_alumno/")
                else:
                    raise Exception("No se pudo obtener el rol del usuario.")

            else:
                raise Exception(response_data["error"]["message"])
        except Exception as e:
            page.snack_bar = SnackBar(
                Text(f"Error: {str(e)}", size=20),
                bgcolor="red"
            )
            page.snack_bar.open = True
        page.update() 

    def registrarse(e: ControlEvent) -> None:
        page.go("/register")

    # Link the functions to our UI
    checkbox_signup.on_change = validate
    text_email.on_change = validate
    text_password.on_change = validate
    submit_button.on_click = submit
    signup_button.on_click = registrarse
    

    return ft.View(
        "/login",
        controls=[
            Column(
                [ft.Text("Login", size=25, weight="bold"),
                text_email,
                text_password,
                checkbox_signup,
                submit_button,
                text_signup,
                signup_button]
            )
        ]
    )

