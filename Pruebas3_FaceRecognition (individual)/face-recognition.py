# Script que, previamente seleccionada una imagen, captura la webcam e identifica o no el rostro del alumno
# Esto sería lo más parecido al sistema. Una vez hecho login, en cada sesión ya se sabe a la foto del alumno con la que se debe comparar, es decir, su "name"

import cv2
import face_recognition

name = "Javi"
# Imagen a comparar
image = cv2.imread("Images/"+name+".jpg")
face_loc = face_recognition.face_locations(image)[0] # Esto devuelve la ubicación (arriba, derecha, abajo, izquierda) del rostro en la imagen
# print("face_loc:", face_loc)

face_image_encodings = face_recognition.face_encodings(image, known_face_locations=[face_loc])[0] # Se generará un vector de características de 128 elementos para cada rostro
# print("face_image_encodings:", face_image_encodings)

# cv2.namedWindow('Image', cv2.WINDOW_NORMAL)

# cv2.rectangle(image, (face_loc[3], face_loc[0]), (face_loc[1], face_loc[2]), (0,255,0),2)
# cv2.imshow("Image", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

######################################################################################
# Video Streaming


print("Capturando rostro...")
cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    if ret == False: break
    frame = cv2.flip(frame, 1)

    face_locations = face_recognition.face_locations(frame)
    if face_locations != []:
        for fl in face_locations:
            face_frame_encodings = face_recognition.face_encodings(frame, known_face_locations=[fl])[0]
            result = face_recognition.compare_faces([face_image_encodings], face_frame_encodings)
            print("Result: ", result)

            if result[0] == True:
                text = name
                color = (125,220,0)
            else:
                text = "Desconocido"
                color = (50,50,255)

            cv2.rectangle(frame, (fl[3], fl[2]), (fl[1], fl[2]+30), color,-1)
            cv2.rectangle(frame, (fl[3], fl[0]), (fl[1], fl[2]), color,2)
            cv2.putText(frame, text, (fl[3], fl[2]+20), 2, 0.7, (255,255,255), 1)

    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    if k == 27 & 0xFF:
        break

cap.release()
cv2.destroyAllWindows()


# El problema de rendimiento que estás experimentando podría deberse a varios factores. Aquí hay algunas sugerencias que podrían ayudarte a solucionar el problema:
# 1. Reducir la resolución de entrada: Si estás procesando un video con alta resolución, intenta reducir la resolución de entrada del video para reducir la carga en el procesamiento. Esto se puede hacer cambiando la resolución del video de entrada o utilizando un método de redimensionamiento de imágenes en el código.
# 2. Utilizar técnicas de optimización de OpenCV: OpenCV tiene muchas técnicas de optimización incorporadas que se pueden utilizar para mejorar el rendimiento. Por ejemplo, puedes intentar utilizar la aceleración de GPU de OpenCV si tu sistema lo soporta. También puedes investigar la utilización de diferentes algoritmos de detección de rostros en OpenCV.
# 3. Probar diferentes técnicas de detección de rostros: Puedes experimentar con diferentes técnicas de detección de rostros para ver cuál funciona mejor en tu situación. Por ejemplo, en lugar de utilizar el método face_recognition.face_locations() y face_recognition.face_encodings(), puedes probar otros métodos de detección de rostros en OpenCV como cv2.CascadeClassifier o utilizar modelos de detección de rostros basados en deep learning como dnn de OpenCV.
# 4. Reducir el tamaño del modelo de detección de rostros: Si estás utilizando un modelo de detección de rostros preentrenado como el utilizado por la biblioteca face_recognition, intenta utilizar un modelo más pequeño o más eficiente para reducir la carga de procesamiento.
# Espero que estas sugerencias te sean útiles para solucionar el problema de rendimiento en tu script de reconocimiento facial.