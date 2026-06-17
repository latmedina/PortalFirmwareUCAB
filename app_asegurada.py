import os
import secrets
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# --- REMEDIACIÓN CRIPTOGRÁFICA (A04: Parche de Confidencialidad) ---
# MEDIDA: Se eliminó la llave estática expuesta en el código (CWE-798).
# Ahora el secreto se lee dinámicamente desde variables de entorno del sistema operativo.
# Si no está definida, se genera una clave criptográficamente fuerte de 32 bytes en tiempo de ejecución.
SECRET_KEY_SISTEMA = os.environ.get("UCAB_PROD_KEY", secrets.token_hex(32))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/config', methods=['GET'])
def get_config():
    # MEDIDA SEGURA: Se deniega la exposición de tokens reversibles o secretos sensibles al cliente.
    # El endpoint solo retorna metadatos operativos genéricos, eliminando la fuga de información técnica.
    return jsonify({
        "status": "online",
        "component": "Core Firmwares v1.0 - Edición Asegurada",
        "debug_mode": False,
        "protected_token_payload": "REDUCIDO: Acceso restringido por política de Privacidad y Mínimo Privilegio."
    })

if __name__ == '__main__':
    print("[*] Iniciando servidor ASEGURADO (Fase I) en el puerto 8080...")
    app.run(host='0.0.0.0', port=8080, debug=False)