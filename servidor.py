from flask import Flask

app = Flask("Servidor")

# endpoint1 - Hola
@app.route("/hello", methods=["GET"])
def funcion_hello():
    return "Hola"

# endpoint2 - Adiós
@app.route("/bye", methods=["GET"])
def funcion_bye():
    return "Adiós"

# Ejecutar el servidor
app.run(port=3690)


# Aquí tendré que definir mis funciones de reconocimiento facial y de OCR
# y establecer los endpoints necesarios 