import requests
from typing import Any, Dict, Optional

BASE_URL = "https://progvanguardia-back.onrender.com/api"

def register_user_api(username: str, email: str, password_hash: str) -> Dict[str, Any]:
    """Llama al endpoint /api/auth/register de Java"""
    url = f"{BASE_URL}/auth/register"
    payload = {
        "username": username,
        "email": email,
        "passwordHash": password_hash,
        "role": "STUDENT"
    }
    response = requests.post(url, json=payload, timeout=20)
    if response.status_code == 201:
        return {"success": True, "data": response.json()}
    else:
        return {"success": False, "error": response.json().get("error", "Error en el registro")}

def login_user_api(email: str, password_raw: str) -> Dict[str, Any]:
    """Llama al endpoint /api/auth/login de Java"""
    url = f"{BASE_URL}/auth/login"
    payload = {
        "email": email,
        "password": password_raw
    }
    response = requests.post(url, json=payload, timeout=5)
    if response.status_code == 200:
        return {"success": True, "data": response.json()}
    else:
        return {"success": False, "error": response.json().get("error", "Credenciales inválidas")}

def ask_orchestrator_api(audit_id: int, prompt: str, user_id: int, language: str = "sql") -> Dict[str, Any]:
    url = f"{BASE_URL}/orchestrator/ask"
    payload = {
        "auditId": int(audit_id),
        "prompt": str(prompt).strip(),
        "userId": int(user_id),
        "language": str(language) # <-- Viaja al mapa de Java
    }
    # ... el resto del código de la función queda exactamente igual ...
    
    try:
        # Hacemos la petición POST al backend de Java
        response = requests.post(url, json=payload, timeout=15)
        
        # Esto va a imprimir en la terminal de VS Code para que lo veas vos en vivo:
        print(f"--- DETECTIVE API --- STATUS CODE: {response.status_code}")
        print(f"--- DETECTIVE API --- RESPONSE TEXT: {response.text}")
        
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            # Si responde un error (400, 500, 404), le mostramos el texto real de Java al usuario
            msg_error = response.text if response.text else f"Código HTTP {response.status_code}"
            return {"success": False, "error": f"Java rechazó la petición: {msg_error}"}
            
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"No se pudo conectar con Java (Error de Red): {str(e)}"}
def fetch_chat_history_api(audit_id: int) -> Optional[Dict[str, Any]]:
    """Trae el historial guardado en MongoDB desde /api/audit/{auditId}/history"""
    url = f"{BASE_URL}/audit/{audit_id}/history"
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        return response.json()
    return None
