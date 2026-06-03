import streamlit as st
from datetime import datetime
from api_client import login_user_api, register_user_api, ask_orchestrator_api, fetch_chat_history_api
from styles import apply_custom_styles
import json
import time 

try:
    from streamlit_ace import st_ace
    ACE_AVAILABLE = True
except ImportError:
    ACE_AVAILABLE = False

# Configuración inicial
st.set_page_config(page_title="Plataforma de Auditoría de Código", layout="wide")
apply_custom_styles()

# Inicialización del Estado de Sesión Global
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_info" not in st.session_state:
    st.session_state.user_info = {}
# Inicialización del Estado de Sesión Global en app.py
if "current_audit_id" not in st.session_state:
    st.session_state.current_audit_id = 300  # <--- Cambialo a 300 para probar un flujo limpio desde cero
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

def render_login_screen():
    st.markdown(
        "<div class='hero-card'>"
        "<h1 class='hero-card-title'>Plataforma de Auditoría vVanguardia</h1>"
        "<p class='hero-card-copy'>Orquestador educativo con persistencia políglota en Supabase y MongoDB Atlas.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    col_left, col_right = st.columns([1.8, 1.2])
    with col_left:
        st.markdown(
            """
            ### ¿Qué puedes hacer en esta versión?
            - **Autenticación Real:** Registro e inicio de sesión conectado a Supabase (Postgres).
            - **Editor Inteligente:** Escribe tus consultas SQL o lógicas con resaltado de sintaxis.
            - **Persistencia en Tiempo Real:** Las consultas y respuestas de la IA se graban en un documento atómico dentro de MongoDB Atlas.
            """
        )

    with col_right:
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.markdown("<span class='login-pill'>CONEXIÓN ACTIVA A JAVA</span>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin:0;'>Acceso al Sistema</h3>", unsafe_allow_html=True)
        
        email = st.text_input("Correo Electrónico", key="ui_email")
        username = st.text_input("Nombre de Usuario (Solo para Registro)", key="ui_user")
        password = st.text_input("Contraseña", type="password", key="ui_pass")

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("Iniciar Sesión", use_container_width=True):
                # Extraemos de forma segura del session_state usando las KEYS correspondientes
                email_val = st.session_state.get("ui_email", "").strip()
                password_val = st.session_state.get("ui_pass", "").strip()

                if email_val and password_val:
                    res = login_user_api(email_val, password_val)
                    if res["success"]:
                        st.session_state.logged_in = True
                        st.session_state.user_info = res["data"]
                        hist = fetch_chat_history_api(st.session_state.current_audit_id)
                        if hist:
                            st.session_state.chat_messages = hist.get("messages", [])
                        st.rerun()
                    else:
                        st.error(res["error"])
                else:
                    st.warning("Completá email y contraseña.")
                    
        with col_b2:
            if st.button("Registrarse", use_container_width=True):
                # Extraemos los tres datos del session_state para el registro
                user_val = st.session_state.get("ui_user", "").strip()
                email_val = st.session_state.get("ui_email", "").strip()
                password_val = st.session_state.get("ui_pass", "").strip()

                if user_val and email_val and password_val:
                    res = register_user_api(user_val, email_val, password_val)
                    if res["success"]:
                        st.success("¡Registrado en Supabase! Iniciá sesión.")
                    else:
                        st.error(res["error"])
                else:
                    st.warning("Completá todos los campos para registrarte.")
        st.markdown("</div>", unsafe_allow_html=True)

def render_dashboard():
    st.sidebar.markdown(f"### 👤 {st.session_state.user_info.get('username')}")
    st.sidebar.markdown(f"**Rol:** `{st.session_state.user_info.get('role')}`")
    st.sidebar.markdown(f"**Auditoría Activa ID:** `{st.session_state.current_audit_id}`")
    
    if st.sidebar.button("Cerrar Sesión", type="secondary"):
        st.session_state.logged_in = False
        st.session_state.chat_messages = []
        st.rerun()

    st.markdown(f"# Panel de Auditoría Académica")
    
    # Selector de lenguaje
    col_lang, _ = st.columns([1, 2])
    with col_lang:
        lang_opciones = {"SQL": "sql", "Java": "java", "Python": "python"}
        lang_seleccionado = st.selectbox("Seleccioná el lenguaje a auditar:", list(lang_opciones.keys()))
        lang_clave = lang_opciones[lang_seleccionado]

    st.markdown("### 💻 Caja de Entrada de Código")
    if ACE_AVAILABLE:
        code_input = st_ace(language=lang_clave, theme="monokai", height=200, font_size=15, key=f"ace_editor_{lang_clave}")
    else:
        code_input = st.text_area("Escribe tu consulta:", height=200, placeholder="Escribe el código aquí...")

    if st.button("Enviar al Orquestador", type="primary"):
        if code_input.strip():
            with st.spinner("Java procesando con la IA y guardando en ambas nubes..."):
                
                nuevo_audit_id = int(time.time() * 1000)
                st.session_state.current_audit_id = nuevo_audit_id
                
                user_id_actual = st.session_state.user_info.get("id", 1)
                
                res = ask_orchestrator_api(st.session_state.current_audit_id, code_input, user_id_actual, lang_clave)
                
                if res["success"]:
                    st.session_state.last_audit = res["data"]
                    st.session_state.chat_messages = res["data"].get("messages", [])
                    st.success(f"¡Auditoría #{nuevo_audit_id} creada con éxito!")
                    st.rerun() 
                else:
                    st.error(res["error"])
        else:
            st.warning("Por favor, ingresa un prompt o código válido.")

    # Mostrar la conversación del hilo conversacional recuperado de Mongo
    st.markdown("---")
    st.markdown("### 💬 Historial Conversacional de la Auditoría (MongoDB Atlas)")
    
    for msg in st.session_state.chat_messages:
        role = msg.get("role")
        content = msg.get("content")
        time_str = msg.get("timestamp", "")[:16].replace("T", " ")
        
        if role == "user":
            with st.chat_message("user"):
                st.write(f"**Alumno ({time_str}):**")
                st.code(content, language=lang_clave)
        else:
            with st.chat_message("assistant"):
                st.markdown(f"**Asistente IA ({time_str}):**")
                
                # Intentamos parsear el contenido por si es el JSON estructurado
                try:
                    data_json = json.loads(content)
                    
                    # Extraemos el puntaje general
                    score = data_json.get("score_general", 0)
                    
                    # Dibujamos una tarjeta visual para el Score
                    if score >= 80:
                        st.success(f"### 🎯 Puntaje de Calidad: {score}/100")
                    elif score >= 50:
                        st.warning(f"### ⚠️ Puntaje de Calidad: {score}/100")
                    else:
                        st.error(f"### 🚨 Puntaje de Calidad: {score}/100")
                    
                    # Iteramos y pintamos cada uno de los hallazgos en acordeones estéticos
                    for finding in data_json.get("findings", []):
                        severity = finding.get("severity", "Info")
                        category = finding.get("category", "General")
                        title = finding.get("title", "Hallazgo")
                        desc = finding.get("description", "")
                        lines = finding.get("affected_lines", "0")
                        fix = finding.get("suggested_fix", "")
                        pedagogical = finding.get("pedagogical_explanation", "")
                        
                        # Definimos el emoji según la gravedad
                        if severity.lower() in ["critico", "crítico", "high"]:
                            emoji = "🚨"
                        elif severity.lower() in ["sugerencia", "info", "low"]:
                            emoji = "💡"
                        else:
                            emoji = "⚠️"
                            
                        # Desplegable premium por cada hallazgo
                        with st.expander(f"{emoji} [{severity.upper()}] {title} ({category})"):
                            st.write(f"**Descripción:** {desc}")
                            st.write(f"📍 **Línea(s) afectada(s):** `{lines}`")
                            
                            if fix:
                                st.markdown("**🔧 Corrección Sugerida:**")
                                st.code(fix, language=lang_clave)
                                
                            if pedagogical:
                                st.markdown("**👨‍🏫 Nota Pedagógica para el Alumno:**")
                                st.info(pedagogical)
                                
                except json.JSONDecodeError:
                    # Si no es un JSON estructurado (un mensaje de chat común), se muestra plano
                    st.info(content)

# Flujo Principal
if st.session_state.logged_in:
    render_dashboard()
else:
    render_login_screen()
