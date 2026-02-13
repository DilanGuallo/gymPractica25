from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import time

# 1. TUS DATOS (Sácalos de la captura que me pasaste)
KEY = "TU_KEY_AQUI"
ENDPOINT = "https://mariosface.cognitiveservices.azure.com/"

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))


def identificar_persona(ruta_foto):
    # Detectar caras en la foto
    with open(ruta_foto, "rb") as img:
        faces = face_client.face.detect_with_stream(img, return_face_attributes=['emotion'])
    
    if not faces:
        print("No se detectó ninguna cara.")
        return

    face_ids = [face.face_id for face in faces]
    
    # Identificar contra nuestro grupo
    results = face_client.face.identify(face_ids, PERSON_GROUP_ID)
    
    for person in results:
        if len(person.candidates) > 0:
            p_id = person.candidates[0].person_id
            socio = face_client.person_group_person.get(PERSON_GROUP_ID, p_id)
            print(f"Socio reconocido: {socio.name}")
            print(f"Emoción: {faces[0].face_attributes.emotion.happiness * 100}% de felicidad")
        else:
            print("Invitado Detectado (Persona no registrada)")

# Prueba con una foto nueva
identificar_persona("entrada_gym.jpg")