import pandas as pd
from datetime import datetime
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials

# --- CONFIGURACIÓN AZURE ---
KEY = "TU_KEY_AQUI"
ENDPOINT = "https://mariosface.cognitiveservices.azure.com/"
PERSON_GROUP_ID = 'gym-socios-v1'
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

# --- CARGAR BASE DE DATOS (Simulada con Excel/CSV local para la demo) ---
# En producción, aquí conectarías con la API de Excel Online
df_socios = pd.read_csv("socios.csv") # O pd.read_excel
df_salas = pd.read_csv("salas.csv")

def procesar_entrada(ruta_foto, nombre_sala, es_invitado=False, socio_anfitrion=None):
    # 1. Detectar Rostro y Emoción
    with open(ruta_foto, "rb") as img:
        faces = face_client.face.detect_with_stream(img, return_face_attributes=['emotion'])
    
    if not faces:
        return "No se detectó rostro."

    face_id = faces[0].face_id
    emocion_actual = faces[0].face_attributes.emotion.happiness

    # 2. Lógica de Aforo
    ocupacion = df_salas.loc[df_salas['Sala'] == nombre_sala, 'OcupacionActual'].values[0]
    capacidad = df_salas.loc[df_salas['Sala'] == nombre_sala, 'CapacidadMax'].values[0]

    if ocupacion >= capacidad:
        return f"ACCESO DENEGADO: La sala {nombre_sala} está llena."

    # 3. Identificación y Reglas de Negocio
    if es_invitado:
        # Validar límite de invitados del socio que lo trae
        invitaciones = df_socios.loc[df_socios['SocioID'] == socio_anfitrion, 'InvitacionesMes'].values[0]
        if invitaciones >= 2:
            return "ACCESO DENEGADO: Socio ya consumió sus 2 invitados."
        
        # Actualizar datos de invitado (Sin guardar foto ni cara)
        df_socios.loc[df_socios['SocioID'] == socio_anfitrion, 'InvitacionesMes'] += 1
        print(f"Invitado registrado para el socio {socio_anfitrion}.")
    
    else:
        # Identificar Socio
        results = face_client.face.identify([face_id], PERSON_GROUP_ID)
        if results and results[0].candidates:
            p_id = results[0].candidates[0].person_id
            nombre_socio = face_client.person_group_person.get(PERSON_GROUP_ID, p_id).name
            print(f"Bienvenido Socio: {nombre_socio}. Felicidad: {emocion_actual}")
        else:
            return "Persona no reconocida. ¿Es usted un invitado?"

    # 4. Actualizar Aforo de la Sala
    df_salas.loc[df_salas['Sala'] == nombre_sala, 'OcupacionActual'] += 1
    
    # Guardar cambios (Simulado)
    # df_salas.to_csv("salas.csv", index=False)
    return "Entrada registrada con éxito."

# --- PRUEBA DE LA DEMO ---
print(procesar_entrada("foto_entrada.jpg", "Musculación"))