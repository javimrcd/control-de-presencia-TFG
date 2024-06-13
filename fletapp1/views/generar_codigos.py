import os
import random
from fpdf import FPDF
from PyPDF2 import PdfMerger
import flet as ft
from flet import ElevatedButton, Text
from flet_route import Params, Basket
from firebase_config import db, bucket
from state import state

codigos_file_path = "views/functions/codigos.txt"

def generar_codigo(alumnos):
    codigos = []
    with open(codigos_file_path, "w") as archivo:
        for _ in range(alumnos):
            codigo = str(random.randint(1000, 9999))
            codigos.append(codigo)
            archivo.write(codigo + "\n")
    return codigos

def generar_pdf(codigo, ruta):
    pdf = FPDF("P", "mm", "Letter")
    pdf.add_page()
    pdf.set_font("helvetica", "", 20)
    pdf.cell(190, 10, codigo, align="C")
    pdf.output(ruta)
    pdf.close()  # Asegúrate de cerrar el archivo después de generarlo

def merge_pdfs(ruta_archivo_final):
    pdf_merger = PdfMerger()
    pdfs_folder = "./PDFS/pdfs_individuales/"

    files = [os.path.join(pdfs_folder, file) for file in os.listdir(pdfs_folder) if os.path.isfile(os.path.join(pdfs_folder, file)) and file.lower().endswith(".pdf")]

    for file in files:
        pdf_merger.append(file)

    output_pdf_path = os.path.abspath(ruta_archivo_final)
    with open(output_pdf_path, 'wb') as appended_pdf:
        pdf_merger.write(appended_pdf)
    pdf_merger.close()  # Cerrar el objeto PdfMerger después de fusionar

    return output_pdf_path

def GenerarCodigos(page: ft.Page, params: Params, basket: Basket):
    user_id = state.user_id
    examen_id = params.get('examen_id')

    def handle_download(e):
        try:
            examen_ref = db.collection('examenes').document(examen_id).get()
            if examen_ref.exists:
                examen_data = examen_ref.to_dict()
                asignatura_ref = examen_data.get('asignatura')
                asignatura_doc = asignatura_ref.get()
                if asignatura_doc.exists:
                    asignatura_data = asignatura_doc.to_dict()
                    num_alumnos = len(asignatura_data.get('alumnos', []))
                    codigos = generar_codigo(num_alumnos)

                    if not os.path.exists('./PDFS/pdfs_individuales'):
                        os.makedirs('./PDFS/pdfs_individuales')

                    for i, codigo in enumerate(codigos):
                        nombre_pdf = f"./PDFS/pdfs_individuales/pdf_{i + 1}.pdf"
                        generar_pdf(codigo, nombre_pdf)

                    ruta_pdf_final = f"./PDFS/codigos_{examen_id}.pdf"
                    merged_pdf_path = merge_pdfs(ruta_pdf_final)

                    # Subir el PDF fusionado a Firebase Storage
                    blob_pdf = bucket.blob(f"usuarios/{user_id}/examenes/{examen_id}/codigos.pdf")
                    blob_pdf.upload_from_filename(merged_pdf_path)
                    blob_pdf.make_public()
                    pdf_url = blob_pdf.public_url

                    # Subir el archivo de texto a Firebase Storage
                    blob_txt = bucket.blob(f"usuarios/{user_id}/examenes/{examen_id}/codigos.txt")
                    blob_txt.upload_from_filename(codigos_file_path)
                    blob_txt.make_public()
                    txt_url = blob_txt.public_url

                    page.snack_bar = ft.SnackBar(
                        ft.Text("PDF y archivo de texto de códigos generados y subidos con éxito", size=20),
                        bgcolor="green"
                    )

                    # Eliminar archivos locales temporales
                    os.remove(codigos_file_path)
                    for file in os.listdir('./PDFS/pdfs_individuales'):
                        os.remove(os.path.join('./PDFS/pdfs_individuales', file))
                    

                else:
                    raise Exception("Asignatura no encontrada.")
            else:
                raise Exception("Examen no encontrado.")
        except Exception as error:
            print(f"Error: {error}")
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Error: {error}", size=20),
                bgcolor="red"
            )
        page.snack_bar.open = True
        page.update()

    volver_button = ElevatedButton(text="Volver", on_click=lambda _: page.go(f"/{user_id}/examenes_profesor"))
    descargar_button = ElevatedButton(text="Descargar PDF códigos", on_click=handle_download)

    return ft.View(
        "/:user_id/examenes_profesor/:examen_id/generar_codigos",
        controls=[
            Text("Generar códigos de acceso", size=25, weight="bold"),
            descargar_button,
            volver_button
        ]
    )
