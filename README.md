# 🏋️‍♂️ Smart Gym: Sistema de Control de Asistencia con IA

Este proyecto consiste en un sistema inteligente para la gestión de socios e invitados de un gimnasio, desarrollado sobre el ecosistema de **Microsoft Azure** y **Power Platform**. El sistema utiliza visión artificial para el control de acceso, gestión de aforo en tiempo real y análisis de bienestar emocional.

---

## 📋 Características del Proyecto

* **Identificación Biométrica:** Reconocimiento facial de socios mediante **Azure AI Face API**.
* **Gestión de Privacidad (Invitados):** Conteo de invitados en tiempo real sin almacenamiento de datos biométricos ni personales, cumpliendo con normativas de privacidad.
* **Control de Aforo Dinámico:** Monitorización de la capacidad máxima en 5 salas distintas.
* **Análisis de Estado de Ánimo:** Registro de expresiones faciales al entrar y salir para medir el impacto del ejercicio en el humor de los socios.
* **Límite de Invitaciones:** Control automático de un máximo de 2 invitados mensuales por socio.

---

## 🏗️ Arquitectura Técnica

El sistema se apoya en los siguientes pilares:

1.  **IA (Cerebro):** [Azure AI Face](https://azure.microsoft.com/es-es/products/ai-services/ai-face) para la detección de rostros, identificación en `PersonGroups` y extracción de atributos de emoción.
2.  **Backend (Administración):** Scripts en **Python** para la creación de la estructura, registro de socios y entrenamiento del modelo.
3.  **App Móvil (Frontend):** **PowerApps** para la captura de imágenes y selección de sala.
4.  **Base de Datos:** **Dataverse / Excel Online** para el seguimiento de aforo y contador de invitaciones.

---

## 📊 Control de Salas y Capacidades

| Sala | Capacidad Máxima |
| :--- | :---: |
| Sala de Musculación | 20 personas |
| Sala de Fitness | 15 personas |
| Piscina | 24 personas |
| Sala de Cycling | 10 personas |
| Cafetería | 40 personas |

---

## 🛠️ Instalación y Configuración

### 1. Requisitos
* Python 3.x instalado.
* Librería de Azure AI Face:
    ```bash
    pip install azure-cognitiveservices-vision-face msrest
    ```
* Clave (Key) y Endpoint de un recurso **Face API** en Azure.

### 2. Preparación del Sistema (Python)
Utiliza el script `config_gym.py` para crear el grupo de socios y entrenar la IA:

```python
# Configura tus credenciales de Azure
KEY = "TU_KEY_AQUI"
ENDPOINT = "[https://tu-recurso.cognitiveservices.azure.com/](https://tu-recurso.cognitiveservices.azure.com/)"
PERSON_GROUP_ID = 'gym-socios-v1'

# El script registra a los alumnos y entrena el modelo de reconocimiento
