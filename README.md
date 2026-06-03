# ProgVanguardia_Front
📌 ¿Qué hace este repositorio?
Este repositorio contiene dos componentes del sistema:
🎨 Frontend — Streamlit (frontend.py)
Panel interactivo que permite al alumno pegar código fuente, enviarlo a auditar y visualizar los hallazgos clasificados por severidad. Mantiene un historial de auditorías previas.
🛠️ Stack Tecnológico
Componente Tecnología
Lenguaje   Python 3.10+
Interfaz de usuario Streamlit
Editor de código streamlit-ace (resaltado sintáctico)
Microservicio IAFastAPI + Uvicorn
Modelo de lenguaje Google Gemini 2.5 Flash
HTTP client requests
Variables de entorno python-dotenv
⚙️ Instalación y Ejecución Local
1. Prerrequisitos

Python 3.10+
pip 23+
API Key de Google Gemini (gratuita)
Backend Java corriendo en http://localhost:8080

2. Clonar el repositorio
git clone https://github.com/MartinAgarcia1710/ProgVanguardia_Front/edit/main
cd python-frontend-ia
3. Instalar dependencias
pip install -r requirements.txt
6. Ejecutar el frontend (Streamlit)
En otra terminal:
streamlit run frontend.py
El navegador abrirá automáticamente http://localhost:8501.
