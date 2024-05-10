import cv2
import os
from deepface import DeepFace

def reconocimiento_facial(nombre_persona):
    cap = cv2.VideoCapture(0)
    imagesFoundPath = "Rostros capturados/"
    max_rostros = 3
    faceClassif = cv2.CascadeClassifier('C:/Programas/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml')
    count = 0

    rostros_capturados_path = "views/functions/Rostros capturados/"
    img_base = "views/functions/Persona/" + nombre_persona + "/" + nombre_persona + ".jpg"

    veredictos_individuales = []
    veredicto_final = False

    capture_face = False

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if capture_face == False:
            faces = faceClassif.detectMultiScale(
                    image=gray_image,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(200,200),
                    maxSize=(1000,1000))
            
            for (x,y,w,h) in faces:
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0),2)

            cv2.namedWindow('frame', cv2.WINDOW_NORMAL)    
            cv2.imshow('frame', frame)

        else:
            if len(faces) > 0:
                for (x,y,w,h) in faces:
                    rostro = frame[y:y+h,x:x+w]
                    rostro = cv2.resize(rostro, (150,150), interpolation=cv2.INTER_CUBIC)
                    cv2.imshow('rostro', rostro)
                    cv2.imwrite(imagesFoundPath+'rostro_{}.jpg'.format(count), rostro)
                    print("Rostro "+'rostro_{}.jpg'.format(count)+" detectado y capturado")
                    count = count + 1
                    capture_face = False
            else:
                capture_face = False
                print("Cuidado, ha pulsado 's' mientras no se detectaba un rostro")
            
        k = cv2.waitKey(1)

        if k == ord('s'):
            capture_face = True

        if k == 27 or count == max_rostros:
            break

    cap.release()
    cv2.destroyAllWindows()

    rostros_capturados = os.listdir(rostros_capturados_path)

    print('Resultados de verificación individuales:')
    for rostro in rostros_capturados:
        resultado_verificacion = DeepFace.verify(
            img1_path=img_base,
            img2_path=rostros_capturados_path+rostro,
            detector_backend="opencv",
            distance_metric="cosine",
            model_name="VGG-Face",
            enforce_detection=False)

        veredictos_individuales.append((rostro, resultado_verificacion['verified']))
        print('Analizando '+f'{rostro}')
        print('Distancia: '+str(resultado_verificacion['distance']))
        print('Umbral: '+str(resultado_verificacion['threshold']))
        print('Veredicto: '+str(resultado_verificacion['verified']))
        print('\n')

    trues = sum(veredicto for (_, veredicto) in veredictos_individuales)
    falses = len(veredictos_individuales) - trues
    veredicto_final = trues > falses

    print('Veredicto final:', veredicto_final)

    if veredicto_final:
        print('La persona identificada es:', nombre_persona)
    else:
        print('La persona identificada NO es:', nombre_persona)

# Ejemplo de uso
# reconocimiento_facial("Javi")
