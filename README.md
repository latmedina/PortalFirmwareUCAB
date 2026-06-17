# Portal de Gestión de Firmwares y Actualizaciones - UCAB

Este proyecto ha sido desarrollado como un entorno de laboratorio práctico para la asignatura de Ciberseguridad en la **Escuela de Ingeniería Informática de la Universidad Católica Andrés Bello (UCAB)**. 

El objetivo principal es simular un escenario real de despliegue de infraestructura crítica (un portal de distribución de firmwares para dispositivos embebidos) para analizar, explotar y posteriormente remediar dos vulnerabilidades críticas del esquema **OWASP Top 10**.

---

## 👥 Integrantes del Equipo
* Luis Medina
* Jesús M.
* Manuel M.
* Sebastián C.

---

## 🛠️ Arquitectura del Proyecto y Tecnologías
Para garantizar el cumplimiento de las directrices de autoría y desarrollo estructural nativo, el sistema se construyó utilizando un stack minimalista sin frameworks pesados ni dependencias externas complejas:
* **Backend:** Python 3 con Flask (Microframework WSGI nativo).
* **Base de Datos:** SQLite 3 (Base de datos relacional local basada en archivos).
* **Frontend:** HTML5, CSS3 y JavaScript Vanilla (UI limpia y scannable).
* **Versionamiento:** Git & GitHub (Estructura rigurosa basada en ramas independientes).

---

## 🗺️ Estructura de Ramas (Git Branching)
El repositorio está dividido estrictamente para demostrar las dos fases del proyecto ante la evaluación docente:

1.  **`main`**: Contiene únicamente este archivo de documentación e instrucciones de despliegue.
2.  **`version-vulnerable`**: Aloja el código original del sistema (`app_vulnerable.py`) donde los controles lógicos están desactivados y expuestos a vectores de ataque.
3.  **`version-asegurada`**: Aloja el código corregido por el Blue Team (`app_asegurada.py`), donde se implementaron las contramedidas criptográficas y de validación matemática.

---

## 🛑 Vulnerabilidades Analizadas (Fase de Explotación)

### 1. OWASP A04:2021 – Cryptographic Failures (Fallos Criptográficos)
* **Ubicación:** Endpoint `/api/config` en `app_vulnerable.py`.
* **Fallo estructural:** El sistema expone un token administrativo de alta jerarquía (`ACCESO_TOTAL_ADMIN_UCAB`). Para intentar "protegerlo", aplica un algoritmo casero basado en una operación matemática XOR simétrica utilizando una clave estática (hardcodeada) visible en el código fuente (`UCAB_KEY_2026`).
* **Impacto:** Rompe el principio de confidencialidad. Cualquier atacante con capacidades de inspección de tráfico o ingeniería inversa puede revertir el payload numérico y secuestrar el token de acceso debido a la simetría del XOR.

### 2. OWASP A08:2021 – Software and Data Integrity Failures (Fallos de Integridad)
* **Ubicación:** Endpoint `/upload-update` en `app_vulnerable.py`.
* **Fallo estructural:** El portal acepta la carga de paquetes de actualización (`.zip` o `.tar`) confiando ciegamente en los metadatos provistos por el cliente. No se realiza verificación de hash seguro (SHA-256) ni validación de firmas digitales.
* **Impacto:** Rompe el principio de integridad. Permite a un atacante inyectar un binario adulterado o un firmware falso modificado con lógica maliciosa, provocando la ejecución o almacenamiento de código arbitrario.

---

## 🛡️ Remediaciones Aplicadas (Fase de Defensa)

### 1. Mitigación contra Fallos Criptográficos (A04)
* **Solución:** Se removió por completo la clave estática del código fuente (mitigando CWE-798). Ahora el secreto operativo del backend se inyecta dinámicamente en memoria a través de **variables de entorno del Sistema Operativo** (`os.environ.get`). 
* Adicionalmente, se restringió el acceso técnico del endpoint `/api/config` aplicando el principio de mínimo privilegio, retornando un código de estado de denegación HTTP 403 ante solicitudes no autorizadas.

### 2. Mitigación contra Fallos de Integridad (A08)
* **Solución:** Se implementó una **lista blanca (whitelist)** rigurosa que valida de forma manual la extensión real del archivo antes de procesarlo.
* Se incorporó el uso de las librerías nativas `hashlib` y `hmac` para leer el flujo de bytes en memoria del archivo subido y calcular en tiempo real su función hash **SHA-256**. El sistema compara este valor mediante `hmac.compare_digest` contra un hash precalulado de un firmware legítimo autorizado por la organización. Si los valores no coinciden milimétricamente, la actualización es abortada por seguridad de la infraestructura.

---

## 🚀 Guía de Despliegue en el Laboratorio (Paso a Paso)

Para replicar el entorno de evaluación virtualizado de forma segura y aislada, se requieren dos Máquinas Virtuales en **VirtualBox** configuradas bajo la misma **"Red Interna"** (`intnet`).

### 📌 Configuración de Direccionamiento IP
* **Máquina Víctima (Ubuntu Server):** `192.168.10.5`
* **Máquina Atacante (Kali Linux):** `192.168.10.10`

---

### 💻 1. Despliegue en la Máquina Víctima (Ubuntu Server)

Una vez iniciado sesión en la terminal de Ubuntu Server, instala las dependencias base necesarias:
```bash
sudo apt update
sudo apt install git python3-pip python3-flask nano -y
