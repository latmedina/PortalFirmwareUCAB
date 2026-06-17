import os
import json
import sqlite3
# pyre: ignore [missing-import]
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# --- CONFIGURACIÓN INSEGURA (OWASP A04: Cryptographic Failures) ---
# CRITICO: Llave estática/hardcodeada expuesta directamente en texto claro dentro del código fuente.
# Esto viola la confidencialidad y permite a un atacante con acceso al código descifrar cualquier secreto.
LLAVE_HARDCODEADA = "UCAB_KEY_2026"

def cifrado_xor_debile(data: str) -> str:
    # Lógica criptográfica casera, obsoleta y vulnerable. 
    # Un cifrado XOR simétrico simple es fácilmente reversible mediante criptoanálisis básico.
    salida = []
    for i in range(len(data)):
        char_data = data[i]
        char_key = LLAVE_HARDCODEADA[i % len(LLAVE_HARDCODEADA)]
        salida.append(chr(ord(char_data) ^ ord(char_key)))
    return "".join(salida)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/config', methods=['GET'])
def get_config():
    # Endpoint vulnerable que expone un token de sesión de alta jerarquía.
    # El secreto del administrador es transmitido usando la función rota de cifrado XOR.
    token_original = "ACCESO_TOTAL_ADMIN_UCAB"
    token_cifrado = cifrado_xor_debile(token_original)
    
    # Convertimos a representación legible (valores unicode en lista) para la simulación del API
    token_payload = [ord(c) for char in token_cifrado]
    
    return jsonify({
        "status": "online",
        "component": "Core Firmwares v1.0",
        "debug_mode": True,
        "protected_token_payload": token_payload,
        "help": "Para recuperar el texto claro, revierte la operación XOR con la llave estática del sistema."
    })


# --- PROCESAMIENTO INSEGURO DE ARCHIVOS (OWASP A08: Software or Data Integrity Failures) ---
@app.route('/upload-update', methods=['POST'])
def upload_update():
    if 'update_file' not in request.files:
        return "[-] Petición inválida: Falta el archivo.", 400
        
    file = request.files['update_file']
    if file.filename == '':
        return "[-] Archivo no seleccionado.", 400

    # CRITICO: Confianza ciega en el cliente. No se valida firma digital (.sig), 
    # no se comprueba hash seguro (SHA-256) ni se valida el tipo real del archivo.
    # Un atacante puede suplantar un firmware legítimo e introducir código malicioso.
    ruta_guardado = os.path.join(".", file.filename)
    file.save(ruta_guardado)
    
    # Simulación del procesador de paquetes que ejecuta la actualización de forma automática
    print(f"[!] Procesando paquete sin verificación de integridad: {file.filename}")
    
    return f"<h3>[+] Actualización '{file.filename}' subida e instalada con éxito en el servidor víctima.</h3><p>Advertencia: El sistema procesó el archivo sin verificar firmas digitales matemáticas.</p><a href='/'>Volver</a>"

if __name__ == '__main__':
    print("[*] Iniciando servidor VULNERABLE en el puerto 8080...")
    app.run(host='0.0.0.0', port=8080, debug=True)