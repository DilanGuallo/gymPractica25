from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import time

# 1. TUS DATOS (Sácalos de la captura que me pasaste)
KEY = "TU_KEY_AQUI"
ENDPOINT = "https://mariosface.cognitiveservices.azure.com/"

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

# ID del grupo (usa minúsculas y guiones)
PERSON_GROUP_ID = 'gym-socios-v1'

def setup_gym():
    try:
        # 2. CREAR EL GRUPO
        print(f"Creando grupo: {PERSON_GROUP_ID}...")
        face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name="Socios Gimnasio")
        
        # 3. CREAR SOCIOS (Tú y tu compañero)
        socios = ["Mario", "Companero_Nombre"]
        
        for nombre in socios:
            person = face_client.person_group_person.create(PERSON_GROUP_ID, nombre)
            print(f"Socio {nombre} creado con ID: {person.person_id}")
            
            # 4. SUBIR FOTO (Asegúrate de tener fotos llamadas mario.jpg, etc. en la misma carpeta)
            try:
                with open(f"{nombre.lower()}.jpg", "rb") as image:
                    face_client.person_group_person.add_face_from_stream(
                        PERSON_GROUP_ID, person.person_id, image)
                print(f"Foto añadida para {nombre}")
            except FileNotFoundError:
                print(f"¡Error! No encontré la foto {nombre.lower()}.jpg")

        # 5. ENTRENAMIENTO (Vital)
        print("Entrenando al modelo...")
        face_client.person_group.train(PERSON_GROUP_ID)

        # Esperar a que termine el entrenamiento
        while True:
            status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
            print(f"Estado: {status.status}")
            if status.status == 'succeeded': break
            time.sleep(1)
            
        print("¡Sistema listo para reconocer socios!")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    setup_gym()