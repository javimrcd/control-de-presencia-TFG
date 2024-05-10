import flet as ft
from flet import TextField, Checkbox, ElevatedButton, Text, Row, Column, SnackBar
from flet_core.control_event import ControlEvent
from flet_route import Params, Basket


def Login(page: ft.Page, params: Params, basket: Basket):
    
    # Setup our fields
    text_username: TextField = TextField(label="Username", text_align=ft.TextAlign.LEFT, width=200)
    text_password: TextField = TextField(label="Password", text_align=ft.TextAlign.LEFT, width=200, password=True)
    checkbox_signup: Checkbox = Checkbox(label="I agree to stuff", value=False)
    submit_button: ElevatedButton = ElevatedButton(text="Submit", width=200, disabled=True)
    hello_button: ElevatedButton = ElevatedButton(text="Hello", width=200)
    identificacion_facial_button: ElevatedButton = ElevatedButton(text="Identificación facial", width=200)


    # functionalities
    def validate(e: ControlEvent) -> None:
        if all([text_username.value, text_password.value, checkbox_signup.value]):
            submit_button.disabled = False
        else:
            submit_button.disabled = True

        page.update()

    def submit(e: ControlEvent) -> None:
        print("Username:", text_username.value)
        print("Password:", text_password.value)

        if(text_password.value == "hola"):
            page.go("/user_id/examenes")
        else:
            page.snack_bar = SnackBar(
                Text("Contraseña incorrecta", size=20),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            
        

    def hello(e: ControlEvent) -> None:
        page.add(
            Row(
                controls=[Text(value="Hello World", size=20)],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )


    # Link the functions to our UI
    checkbox_signup.on_change = validate
    text_username.on_change = validate
    text_password.on_change = validate
    submit_button.on_click = submit
    hello_button.on_click = hello

    # Render our sign-up page
    # page.add(
    #     Row(
    #         controls=[
    #             Column(
    #                 [text_username,
    #                  text_password,
    #                  checkbox_signup,
    #                  submit_button]
    #             )
    #         ],
    #         alignment=ft.MainAxisAlignment.CENTER
    #     )
    # )

    return ft.View(
        "/login",
        controls=[
            Column(
                [ft.Text("Login", size=25, weight="bold"),
                text_username,
                text_password,
                checkbox_signup,
                submit_button]
            )
        ]
    )

# if __name__ == '__main__':
#     ft.app(target=Login)


