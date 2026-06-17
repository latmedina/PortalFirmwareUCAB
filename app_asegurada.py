import os
import hmac
import hashlib
import secrets
from flask import Flask, request, render_template

app = Flask(__name__)

# Clave criptográfica para HMAC o verificación simulada leída de entorno seguro
SECRET_KEY_SISTEMA = os.environ.get("UCAB_PROD_KEY", secrets.token_hex(32)).encode()

# Hash SHA-256 de simulación precalulado y autorizado que representa un firmware legítimo
# Evita que cualquier binario adulterado sea interpretado (Mitigación OWASP A08)
HASH_AUTORIZADO_EJEMPLO = "8543d83151f4961b7f94e24ef2a1e1236f04c6e7f22312b6f123456789abcdef"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/config', methods=['GET'])
def get_config():
    return "Acceso restringido.", 403

# --- REMEDIACIÓN DE INTEGRIDAD (A08: Parche de Validación de Software) ---
@app.route('/upload-update', methods=['POST'])
def upload_update():
    if 'update_file' not in request.files:
        return "[-] Petición no válida", 400
        
    file = request.files['update_file']
    if file.filename == '':
        return "[-] Archivo no seleccionado", 400

    # Medida 1: Validación estricta y manual de la extensión real ( whitelist )
    extensiones_permitidas = ('.zip', '.tar')
    if not file.filename.endswith(extensiones_permitidas):
        return "<h3>[-] Error Crítico (CWE-434): Extensión de archivo denegada. Solo se admiten actualizaciones estructuradas .zip o .tar</h3>", 403

    try:
        # Leemos el flujo de bytes directamente en memoria para realizar el cálculo matemático
        contenido_bytes = file.read()
        
        # Medida 2: Cálculo manual del hash SHA-256 del archivo recibido (CWE-494)
        hash_calculado = hashlib.sha256(contenido_bytes).hexdigest()
        
        # Simulación de control: Verificamos si el hash coincide de manera exacta con el firmware aprobado por la organización
        # En producción real, aquí se verificaría la Firma Digital usando la llave pública del fabricante
        if not hmac.compare_digest(hash_calculado, HASH_AUTORIZADO_EJEMPLO):
            print(f"[-] INTENTO DE INTRUSIÓN DETECTADO: Hash matemático no coincide ({hash_calculado})")
            return f"<h3>[-] Alerta de Seguridad (OWASP A08): Intento de ruptura de integridad. El hash calculado no corresponde a una firma digital autorizada por el Red Team de la UCAB.</h3>", 40d
            
        # Si pasa los controles de integridad, procedemos con el almacenamiento seguro
        ruta_segura = os.path.join("/tmp", os.path.basename(file.filename))
        with open(ruta_segura, "wb") as f:
            f.write(contenido_bytes)
            
        return "<h3>[+] Validación Matemática Completa: Paquete procesado de forma íntegra y segura.</h3>"
        
    except Exception as e:
        # Bloque controlado try/except para evitar la fuga de errores descriptivos internos (OWASP A10)
        return "[-] Ocurrió un error interno controlado durante el procesamiento del firmware.", 500

if __name__ == '__main__':
    print("[*] Iniciando servidor SECURE CENTRAL en modo producción...")
    app.run(host='0.0.0.0', port=8080, debug=False)