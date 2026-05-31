# Requisitos de instalación:
# pip install streamlit requests streamlit-ace
# Ejecutar la aplicación localmente:
# streamlit run frontend.py

import concurrent.futures
from datetime import datetime
from typing import Any, Dict, List

import requests
import streamlit as st

try:
    from streamlit_ace import st_ace
    ACE_AVAILABLE = True
except ImportError:
    ACE_AVAILABLE = False

BACKEND_AUDIT_URL = "http://localhost:8080/api/audits"
BACKEND_HISTORY_URL = "http://localhost:8080/api/audits/history"

st.set_page_config(
    page_title="Plataforma de Auditoría de Código",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #0f172a 0%, #111827 40%, #1f2937 100%);
        color: #f8fafc;
    }
    .login-box {
        background: rgba(15, 23, 42, 0.88);
        padding: 2rem;
        border-radius: 1rem;
        border: 1px solid rgba(148, 163, 184, 0.18);
    }
    .sidebar .sidebar-content {
        background: rgba(15, 23, 42, 0.92);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def initialize_session() -> None:
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "last_audit" not in st.session_state:
        st.session_state.last_audit = None
    if "audit_history" not in st.session_state:
        st.session_state.audit_history = []
    if "backend_message" not in st.session_state:
        st.session_state.backend_message = ""


def login_user() -> None:
    st.session_state.logged_in = True



def render_login_screen() -> None:
    st.markdown("# Plataforma de Auditoría de Código")
    st.markdown("### Bienvenido. Ingresa para comenzar a auditar tus consultas SQL.")
    st.markdown(
        """
        Esta interfaz simula el flujo de sesión local.
        El backend de Java aún no controla el login real, por lo que la sesión se mantiene
        en el frontend hasta que se cierre la aplicación.
        """
    )

    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.markdown(
            """
            #### ¿Qué puedes hacer?
            - Pegar tu consulta SQL en un editor de código estilizado.
            - Presionar `Auditar Código` para enviar la consulta.
            - Ver resultados clasificados por severidad.
            - Revisar el historial de auditorías en la barra lateral.
            """
        )

    with col_right:
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.subheader("Acceso a la plataforma")
        st.text_input("Usuario", key="login_username")
        st.text_input("Contraseña", type="password", key="login_password")
        st.write("")
        if st.button("Iniciar Sesión", type="primary"):
            login_user()
        if st.button("Registrarse"):
            st.success("Registro simulado completado. Ahora pulsa Iniciar Sesión.")
        st.markdown("</div>", unsafe_allow_html=True)


def fetch_audit_history() -> List[Dict[str, Any]]:
    try:
        response = requests.get(BACKEND_HISTORY_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict):
            return data.get("history", data.get("audits", []))
        if isinstance(data, list):
            return data
    except requests.exceptions.RequestException:
        st.sidebar.warning(
            "No se pudo cargar el historial del backend. Mostrando datos de auditoría simulados."
        )
    return [
        {
            "audit_date": "2026-05-29T16:40:00",
            "status": "COMPLETED",
            "summary": "Revisión de inyección SQL detectada",
            "findings": 2,
        },
        {
            "audit_date": "2026-05-28T11:12:00",
            "status": "COMPLETED",
            "summary": "Análisis de sintaxis y seguridad",
            "findings": 1,
        },
    ]


def render_history_sidebar(history: List[Dict[str, Any]]) -> None:
    st.sidebar.header("Historial de Auditorías")
    st.sidebar.markdown(
        "Aquí se listan las auditorías previas. Selecciona una para ver el resumen rápido."
    )

    if not history:
        st.sidebar.info("No hay auditorías previas disponibles.")
        return

    for item in history:
        audit_date = item.get("audit_date") or item.get("date") or "Sin fecha"
        status = item.get("status", "PENDIENTE")
        summary = item.get("summary", "Auditoría de código")
        expand_label = f"{format_audit_date(audit_date)} · {status}"
        with st.sidebar.expander(expand_label):
            st.write(f"**Resumen:** {summary}")
            if item.get("findings") is not None:
                st.write(f"**Hallazgos:** {item['findings']}")
            if item.get("duration"):
                st.write(f"**Duración:** {item['duration']}")
            if item.get("details"):
                st.write(f"**Detalles:** {len(item['details'])} hallazgos registrados")


def format_audit_date(audit_date: str) -> str:
    try:
        parsed = datetime.fromisoformat(audit_date)
        return parsed.strftime("%d/%m/%Y %H:%M")
    except ValueError:
        return audit_date


def render_code_editor(initial_value: str = "") -> str:
    if ACE_AVAILABLE:
        return st_ace(
            value=initial_value,
            language="sql",
            theme="monokai",
            key="sql_editor",
            height=320,
            font_size=16,
            tab_size=4,
            wrap=True,
            min_lines=12,
            placeholder="Pega aquí tu consulta o script SQL...",
        )

    return st.text_area(
        "Pega tu consulta SQL aquí:",
        value=initial_value,
        height=320,
        key="sql_editor",
        placeholder="Pega aquí tu código SQL...",
        help="Si no está instalado streamlit-ace, se usa un editor de texto alternativo.",
        max_chars=30000,
    )


def post_audit_request(sql_query: str) -> requests.Response:
    return requests.post(
        BACKEND_AUDIT_URL,
        json={"sql_query": sql_query},
        timeout=12,
    )


def render_severity_card(finding: Dict[str, Any]) -> None:
    severity = str(finding.get("severity", "UNKNOWN")).upper()
    line_number = finding.get("line_number", "-")
    issue_type = finding.get("issue_type", "Tipo no especificado")
    explanation = finding.get("explanation", "No se proporcionó una explicación.")

    content = (
        f"**Línea:** {line_number}  \n"
        f"**Tipo:** {issue_type}  \n"
        f"**Explicación:** {explanation}"
    )

    if severity in {"CRITICAL", "CRÍTICO"}:
        st.error(f"**{severity}**\n\n{content}")
    elif severity in {"WARNING", "ADVERTENCIA"}:
        st.warning(f"**{severity}**\n\n{content}")
    elif severity in {"SUGGESTION", "SUGERENCIA"}:
        st.info(f"**{severity}**\n\n{content}")
    else:
        st.info(f"**{severity}**\n\n{content}")


def render_audit_results(result: Dict[str, Any]) -> None:
    st.markdown("---")
    st.subheader("Resultados de la Auditoría")
    if not result:
        st.info("No se han recibido resultados aún. Presiona 'Auditar Código' para iniciar una revisión.")
        return

    details = result.get("details") or []
    summary = result.get("summary") or "Resultados procesados"
    st.markdown(f"**Resumen:** {summary}")

    if not details:
        st.success("No se detectaron hallazgos críticos. Tu consulta pasó la auditoría inicial.")
        return

    for finding in details:
        render_severity_card(finding)


def render_dashboard() -> None:
    st.markdown("# Panel de Auditoría de Código")
    st.markdown(
        "Bienvenido al panel principal. Aquí puedes pegar tu consulta SQL, auditarla y revisar hallazgos de seguridad y calidad."
    )

    history = fetch_audit_history()
    render_history_sidebar(history)

    columns = st.columns([3, 1])
    with columns[0]:
        st.markdown("### Editor de Código SQL")
        sql_query = render_code_editor()

        if st.button("Auditar Código", type="primary"):
            if not sql_query or not sql_query.strip():
                st.error("Por favor, ingresa una consulta SQL antes de auditar.")
            else:
                try:
                    with st.spinner("Enviando consulta al orquestador de auditoría..."):
                        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                            future = executor.submit(post_audit_request, sql_query)
                            response = future.result()

                    if response.status_code == 200:
                        st.session_state.last_audit = response.json()
                        st.success("Auditoría completada con éxito.")
                    else:
                        st.session_state.last_audit = None
                        st.error(
                            f"El backend respondió con estado {response.status_code}. "
                            "Verifica el servicio Java y vuelve a intentar."
                        )
                except requests.exceptions.ConnectionError:
                    st.session_state.last_audit = None
                    st.error(
                        "No se pudo conectar con el backend Java "
                        "Asegúrate de que el servicio esté activo y vuelve a intentar."
                    )
                except requests.exceptions.RequestException as error:
                    st.session_state.last_audit = None
                    st.error(f"Ocurrió un error al auditar: {error}")

        render_audit_results(st.session_state.last_audit or {})

    with columns[1]:
        st.markdown("### Estado del Sistema")
        st.info("")
        st.markdown("**Flujo de sesión:** Simulado con `st.session_state`.")
        st.markdown("**Editor:** Sintaxis SQL y tipografía monospace.")
        if ACE_AVAILABLE:
            st.success("")
        else:
            st.warning(
                "Editor alternativo activo. Instala `streamlit-ace` para resaltado de sintaxis."
            )

        if st.button("Cerrar Sesión", type="secondary"):
            st.session_state.logged_in = False


def main() -> None:
    initialize_session()
    if st.session_state.logged_in:
        render_dashboard()
    else:
        render_login_screen()


if __name__ == "__main__":
    main()
